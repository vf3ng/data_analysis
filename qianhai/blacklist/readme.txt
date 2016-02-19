Java KeyStore文件转换为微软的.pfx文件和OpenSSL的PEM格式文件(.key + .crt)

运行方式：
JKS2PFX <KeyStore文件> <KeyStore密码> <Alias别名> <导出文件名> [Java Runtime的目录]

Java Runtime的目录，指包含Java.exe和keytool.exe的目录，如：
c:\progra~1\Java\jre1.5.0_06\bin

例如：
JKS2PFX server.jks 123456 tomcat exportfile c:\progra~1\Java\jre1.5.0_06\bin


www.myssl.cn
2006.5.29