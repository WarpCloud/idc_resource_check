# -*- coding: utf-8 -*-

LOGGER_LOC = "/tmp/idc_resource.log"

# prometheus url
PROMETHEUS_URL = "http://127.0.0.1:31601"
NAMESPACE = "1ofnuao,2xxech7,58ubu0z,678g06d,6dpegds,9qfqiiz,aoiag98,appmarket,dataplatform,helmv3,imn0omj,nanjing-demo,s8gt4zt,swnc13p,tdcsys,tvigufi,uq7ceh2,v49eze4"
#NAMESPACE = "1ofnuao"

# PROMETHEUS_URL = "http://172.26.0.51:31601"
# NAMESPACE = "aquila-do-not-delete,cicd,common,inceptor-integ1,inceptor-integ2,nightly-trunk-test,shared-env,shared-env-safe,ut"


# 过去多长时间进行统计
LAST_DURATION_TIME = "600s"



NAMESPACE_BLACK_LIST = "kube-system,rook-ceph,monitor,kube-public,default"

EXPORT_EXCEL_PATH_NAME = "./idc_resource.xls"