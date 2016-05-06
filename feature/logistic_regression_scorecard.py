#-*-coding: utf-8-*-

from sklearn.linear_model import LogisticRegression as LR

from compute_iv_from_datafile import *

'''
合并区间的试算过程
tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
good_data = get_merge_data('data/f_good','data/f_done')
bad_data = get_merge_data('data/f_delay')

def common_feature_iv(table_name, feature_name, bins, user_id = 'user_id'):
    sql_1, sql_0, relation_type = IV_sql_list[2]
    id_list_1 = tk_yufa.get_id_list(sql_1)
    id_list_0 = tk_yufa.get_id_list(sql_0)
    feature_1 = data_online.get_common_feature(date, id_list_1, 'nothing', table_name, feature_name, bins = bins, user_id = user_id)[3]
    feature_0 = data_online.get_common_feature(date, id_list_0, 'nothing', table_name, feature_name, bins = bins, user_id = user_id)[3]
    total_1 = feature_1.sum()
    total_0 = feature_0.sum()
    IV = 0
    for i in range(len(feature_1)):
        if feature_1[i] == 0 or feature_0[i] == 0:
            continue
        IV = (feature_1[i]*1.0/total_1-feature_0[i]*1.0/total_0)*math.log((feature_1[i]*1.0/total_1)/(feature_0[i]*1.0/total_0)) + IV
    print IV
    a = pd.concat([feature_1,feature_0],axis=1,keys = ['good','bad'])
    a['rate'] = a['good']/a['bad']
    return a

print common_feature_iv('ebusiness_feature', 'total_price', bins = [0,3000,6000,9000,12000,21000,24000,27000])
'''

good_data = get_merge_data('data/f_good','data/f_done')
bad_data = get_merge_data('data/f_delay')
good_data['y'] = 1
bad_data['y'] = 0
good_bad_data = pd.concat([good_data[0:2000], bad_data[0:2000]]) 

pass_data = get_merge_data('data/f_pass')
reject_data = get_merge_data('data/f_reject')
pass_data['y'] = 1
reject_data['y'] = 0
pass_reject_data = pd.concat([pass_data, reject_data])

def get_feature_woe(feature_name, bins=None):
    if bins == None:
        good = fetch_feature_interval_frequency(good_data, feature_name, feature_bins_dict[feature_name])
        bad = fetch_feature_interval_frequency(bad_data, feature_name, feature_bins_dict[feature_name])
    else:
        good = fetch_feature_interval_frequency(good_data, feature_name, bins)
        bad = fetch_feature_interval_frequency(bad_data, feature_name, bins)
    a = pd.concat([good,bad],axis=1,keys = ['good','bad'])
    #a['rate'] = a['good']/a['bad']
    g_sum = a['good'].sum()
    b_sum = a['bad'].sum()
    a['woe'] = (a['good']/g_sum)/(a['bad']/b_sum)
    return a


woe_dict = {
            'call_count_per_day' : get_feature_woe('call_count_per_day',[0,3,6,9,12,24]),
            'phone_loan_times_per_platform' : get_feature_woe('phone_loan_times_per_platform',[0,1,3,4,5,6]),
            'idcard_loan_platform_num' : get_feature_woe('idcard_loan_platform_num',[0,3,12,15,18,21]),
            'idcard_loan_times_per_platform' : get_feature_woe('idcard_loan_times_per_platform',[0,1,2,3,5,6])
           }


def value_to_woe(value, feature_name):
    index = woe_dict[feature_name].index
    temp = [list(map(float,i[1:-1].split(','))) for i in index]
    for i in range(len(index)-1):
        if value >= temp[i][0] and value <temp[i][1]:
            return woe_dict[feature_name]['woe'][index[i]]
    return woe_dict[feature_name]['woe'][index[-1]]

#将数组转化为对应的woe值
good_bad_data['call_count_per_day_woe'] = good_bad_data['call_count_per_day'].map(lambda value: value_to_woe(value, 'call_count_per_day'))
good_bad_data['phone_loan_times_per_platform_woe'] = good_bad_data['phone_loan_times_per_platform'].map(lambda value: value_to_woe(value, 'phone_loan_times_per_platform'))
good_bad_data['idcard_loan_platform_num_woe'] = good_bad_data['idcard_loan_platform_num'].map(lambda value: value_to_woe(value, 'idcard_loan_platform_num'))
good_bad_data['idcard_loan_times_per_platform_woe'] = good_bad_data['idcard_loan_times_per_platform'].map(lambda value: value_to_woe(value, 'idcard_loan_times_per_platform'))

pass_reject_data['call_count_per_day_woe'] = pass_reject_data['call_count_per_day'].map(lambda value: value_to_woe(value, 'call_count_per_day'))
pass_reject_data['phone_loan_times_per_platform_woe'] = pass_reject_data['phone_loan_times_per_platform'].map(lambda value: value_to_woe(value, 'phone_loan_times_per_platform'))
pass_reject_data['idcard_loan_platform_num_woe'] = pass_reject_data['idcard_loan_platform_num'].map(lambda value: value_to_woe(value, 'idcard_loan_platform_num'))
pass_reject_data['idcard_loan_times_per_platform_woe'] = pass_reject_data['idcard_loan_times_per_platform'].map(lambda value: value_to_woe(value, 'idcard_loan_times_per_platform'))


lr = LR()

def get_logistic_func(X, y):
    lr.fit(X, y)
    def logistic_func(*args):
        return 1/(1+np.exp(-(lr.intercept_[0] + (lr.coef_.ravel()*np.array(args)).sum())))
    return logistic_func

def get_scorecard(logistic_func, b = 500 , o = 1, p = 20):
    def scorecard(*args):
        return p/np.log(2)*np.log(logistic_func(*args)/(1-logistic_func(*args)))-p*np.log(o)/np.log(2)+b
    return scorecard

if __name__ == '__main__':
    
    #平测模型的好坏（类似交叉验证）
    test_result = []
    for i in range(10):
        num = int(len(good_bad_data)*0.7)
        random_index = np.random.permutation(len(good_bad_data))    
        build_index = random_index[:num]
        test_index = random_index[num:]
        X = np.array(good_bad_data[['call_count_per_day_woe', 'phone_loan_times_per_platform_woe', 'idcard_loan_platform_num_woe', 'idcard_loan_times_per_platform_woe']].iloc[build_index])
        y = np.array(good_bad_data['y'].iloc[build_index])
        X_test = np.array(good_bad_data[['call_count_per_day_woe', 'phone_loan_times_per_platform_woe', 'idcard_loan_platform_num_woe', 'idcard_loan_times_per_platform_woe']].iloc[test_index])
        y_test = np.array(good_bad_data['y'].iloc[test_index])
        logistic_func = get_logistic_func(X, y)
        test_result.append([lr.score(X,y),lr.score(X_test,y_test)])
    print np.array(test_result).mean(axis=0),lr.coef_

    #平测模型的好坏
    test_result = []
    for i in range(10):
        num = int(len(pass_reject_data)*0.7)
        random_index = np.random.permutation(len(pass_reject_data))
        build_index = random_index[:num]
        test_index = random_index[num:]
        X1 = np.array(pass_reject_data[['call_count_per_day_woe', 'phone_loan_times_per_platform_woe', 'idcard_loan_platform_num_woe', 'idcard_loan_times_per_platform_woe']].iloc[build_index])
        y1 = np.array(pass_reject_data['y'].iloc[build_index])
        X1_test = np.array(pass_reject_data[['call_count_per_day_woe', 'phone_loan_times_per_platform_woe', 'idcard_loan_platform_num_woe', 'idcard_loan_times_per_platform_woe']].iloc[test_index])
        y1_test = np.array(pass_reject_data['y'].iloc[test_index])
        logistic_func = get_logistic_func(X1, y1)
        test_result.append([lr.score(X,y),lr.score(X_test,y_test)])
    print np.array(test_result).mean(axis=0),lr.coef_

    
    #观察评分卡函数效果(pass_reject)
    X_all = np.array(pass_reject_data[['call_count_per_day_woe', 'phone_loan_times_per_platform_woe', 'idcard_loan_platform_num_woe', 'idcard_loan_times_per_platform_woe']])
    y_all = np.array(pass_reject_data['y'])
    logistic_func = get_logistic_func(X_all, y_all)
    scorecard = get_scorecard(logistic_func)
    score = []
    for i in np.random.permutation(len(X_all)):
        score.append((int(scorecard(*X_all[i])),y_all[i]))
    print score
    

    '''
    可以自己编写测试正确率的函数
    right_num = 0
    X_test = data.iloc[test_index]
    y_test = data.iloc[test_index]
    for i in range(len(X_test)):
        if logistic_func(X_test['call_count_per_day_woe'].iloc[i], X_test['phone_loan_times_per_platform_woe'].iloc[i], X_test['idcard_loan_platform_num_woe'].iloc[i], X_test['idcard_loan_times_per_platform_woe'].iloc[i])>=0.5:
            if y_test['y'].iloc[i] == 1:
                right_num += 1
        else:
            if y_test['y'].iloc[i] == 0:
                right_num += 1
    print '测试正确率: ',right_num*1.0/len(X_test)
    '''

  
        

