#-*- coding: utf-8 -*-

from compute_feature import *

#计算IV值用的区间可能和Bi展示用的区间不一致，因为数据量的问题计算IV时有时会合并一些区间
feature_bins_dict = {
                        'call_count':range(0,6501,500),
                        'call_time':range(0,420001,30000),
                        'sustained_days':range(0,181,30),                         
                        'call_count_per_day':range(0,28,3),                         
                        'baidu_home_distance':range(0,72001,6000),                         
                        'baidu_work_distance':range(0,72001,6000),                         
                        'getui_home_distance':range(0,100001,10000),                                            
                        'getui_work_distance':range(0,100001,10000),                         
                        'phone_loan_platform_num':range(0,22,3),                         
                        'phone_loan_times':range(0,101,10),                         
                        'phone_loan_times_per_platform':range(0,7,1),                         
                        'idcard_loan_platform_num':range(0,22,3), 
                        'idcard_loan_times':range(0,101,10), 
                        'idcard_loan_times_per_platform':range(0,7,1) 
                    }


def get_merge_data(*args):
    datalist=[]
    for filename in args:
        datalist.append(pd.read_table(filename))
    return pd.concat(datalist)    

def fetch_feature_interval_frequency(dataframe, feature_name, bins):
    data = dataframe[feature_name]
    if data.dtype ==object:
        data = data[(data!='parents_True')&(data!='Nonesuspect_False')&(data!='parents_None')&(data!='parents_False')]
    data = data.map(float)
    data = data[data!=-1]
    cut = pd.cut(data, bins, right = False)
    cut = cut.replace(np.nan, '[%s, inf)'%bins[-1])
    new_index = ['[%s, %s)'%(bins[i],bins[i+1]) if i!=len(bins)-1 else '[%s, inf)'%bins[i] for i in range(len(bins))]    
    result = cut.value_counts().reindex(new_index).fillna(0)
    return result


if __name__ =='__main__':

    start = time.time()

    data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)    
    good_data = get_merge_data('data/f_good','data/f_done')
    bad_data = get_merge_data('data/f_delay')
    pass_data = get_merge_data('data/f_pass')
    reject_data = get_merge_data('data/f_reject')
    m_data = get_merge_data('data/f_delay','data/f_done')
    not_m_data = get_merge_data('data/f_good')
    
    for feature_name in feature_bins_dict:
        Pass = fetch_feature_interval_frequency(pass_data, feature_name, feature_bins_dict[feature_name])
        reject = fetch_feature_interval_frequency(reject_data, feature_name, feature_bins_dict[feature_name])
        m = fetch_feature_interval_frequency(m_data, feature_name, feature_bins_dict[feature_name])
        not_m = fetch_feature_interval_frequency(not_m_data, feature_name, feature_bins_dict[feature_name])
        good = fetch_feature_interval_frequency(good_data, feature_name, feature_bins_dict[feature_name])
        bad = fetch_feature_interval_frequency(bad_data, feature_name, feature_bins_dict[feature_name])
        data_online.compute_IV(feature_name, 'pass_reject', Pass, reject)
        data_online.compute_IV(feature_name, 'm_not_m', m, not_m)
        data_online.compute_IV(feature_name, 'good_bad', good, bad)
    
    data_online.commit_and_close()
    print time.time()-start


