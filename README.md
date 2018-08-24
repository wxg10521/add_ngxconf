### add_ngxconf
####必须要用python 2.7
阿里云控制台申请 "Access Key" ，并修改脚本中的 "ID" 与 "Secret"
推荐创建子用户建议访问控制RAM，创建相应的最小全向：
{
  "Version": "1",
  "Statement": [
    {
      "Action": "alidns:*",
      "Resource": "acs:alidns:*:*:domain/xiaoyun.com",
      "Effect": "Allow"
    }
  ]
}
pip install aliyun-python-sdk-httpdns==2.1.0
pip install aliyun-python-sdk-domain
pip install aliyun-python-sdk-alidns
pip install aliyun-python-sdk-ecs
