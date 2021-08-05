# coding=UTF-8
'''
@Copyright: Copyright (c) Huawei Technologies Co., Ltd. 2012-2018. All rights reserved.
@Description:
@Author: wwx875840
@Date: 2021/5/26  11:15
'''

import requests, json, datetime, sys, getopt

branch = sys.argv[1]

GT_URL = "http://goldentower.inhuawei.com/api/v2/config?configName={}&group=unc".format(branch)
# 海外区版本号
version = '21.3.0.88'
# 中国区版本号
chs_version = '20.5.2.88'
# 基线分支
base_branch = 'feature/21.3.rc1_tr5_release'

# 基线artifactry的转release的version
base_arti_version = '21.3.RC1.TR5.6'
# 前补丁分支
pre_arti_branch = 'feature/hotpatch/21.3.rc1_release_patch_sph5'
# 前补丁artifactry的转release的version
pre_arti_version = '21.3.RC1.5.1'
# sf套餐的cmc版本号
sf_cmc_version = 'ServiceFabric 21.3.RC1.5.B004'
# 版本归档cmc的海外区路径
archive_cmc_version = 'UNC 21.3.RC1.5.B005'
# 版本归档cmc的中国区路径
archive_chs_cmc_version = 'UNC 20.6.0.5.B004'

# 本次构建补丁单元
build_patch_unit = ['am', 'sm', 'apppub', 'nrf', 'sbim', 'sbim-obj']

# 本次有无资源补丁(类型区分SF/UNC/no)
omres_pat_type = 'sf'


def get_gt_info(branch):
    resp = requests.get(url=GT_URL)
    with open('./package.json', 'w', encoding='utf-8') as f:
        json.dump(resp.json(), f)
    return resp


def mod_pre_gt_info(branch):
    resp = get_gt_info(branch).json()
    data = resp['config']

    '''
    修改有前补丁和basebranch的金字塔配置
    '''

    '''1、修改version页签'''
    for i in data['product']:
        if i['scenario'] == 'default':
            i['appVersion'] = version
            i['interfaceId'] = version
            i['data']['appVersion'] = version
            i['data']['interfaceId'] = version

        if i['scenario'] == 'china':
            i['appVersion'] = chs_version
            i['interfaceId'] = version
            i['data']['appVersion'] = version
            i['data']['interfaceId'] = version
            i['modOriginFromPatch'] = '20.5.2.10'
            i['modOriginFromBase'] = '20.5.2'

    for i in data['artiArchive']:
        if i['scenario'] == 'default':
            i['version'] = version + '-SNAPSHOT'
            i['data']['version'] = version + '-SNAPSHOT'
        if i['scenario'] == 'china':
            i['version'] = chs_version + '-SNAPSHOT'
            i['data']['version'] = chs_version + '-SNAPSHOT'

    '''2、修改金字塔repo页签'''
    for i in data['repo']:
        if i['__product'] == 'unc':
            i['flag'] = branch

    '''3、修改金字塔的arti页签'''
    for j in data['arti']:
        """omres、omadapter、trace、u2000修改"""
        if j['__product'] == 'unc' and 'china' not in j['name']:
            if 'omres' in j['name'] or 'cspadapterunc' in j['name'] or 'upgradeunc' in j['name'] or 'traceunc' in j[
                'name'] or 'u2000unc' in j['name']:
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = version + '-SNAPSHOT'

        if j['__product'] == 'unc' and 'china' in j['name']:
            if 'omres' in j['name'] or 'cspadapterunc' in j['name'] or 'upgradeunc' in j['name'] or 'traceunc' in j[
                'name'] or 'u2000unc' in j['name']:
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = chs_version + '-SNAPSHOT'

        """patch标签修改"""
        if j['__product'] == 'unc' and j['groupId'] == 'com.huawei.5gcore.feature':
            if j['name'] in build_patch_unit:
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = version + '-SNAPSHOT'
            if j['name'].replace('_china', '') in build_patch_unit:
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = chs_version + '-SNAPSHOT'
            if j['name'] in ['patch', 'patch-etsi', 'patch-xsf', 'hotpatch', 'hotpatch-vnfcpatch', 'hotpatch-etsi',
                             'hotpatch-xsf']:
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = version + '-SNAPSHOT'
            if j['name'] in ['patch_china', 'patch-etsi_china', 'patch-xsf_china', 'hotpatch_china',
                             'hotpatch-vnfcpatch_china', 'hotpatch-etsi_china', 'hotpatch-xsf_china']:
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = chs_version + '-SNAPSHOT'
            if j['name'] in ['acs_patch', 'acs_vnfc'] and omres_pat_type == 'sf':
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = version + '-SNAPSHOT'
            if j['name'] in ['acs_patch', 'acs_vnfc'] and omres_pat_type == 'unc':
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = version + '-SNAPSHOT'

            '''冷补丁模板修改'''
            if 'template_vnfd' in j['name']:
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = version + '-SNAPSHOT'
            if 'template_vnfd_china' in j['name']:
                j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
                j['version'] = chs_version + '-SNAPSHOT'

    '''4、修改金字塔的cmc页签'''
    for i in data['cmc']:
        if i['name'] == 'ServiceFabric 30':
            i['version'] = sf_cmc_version

    '''5、修改金字塔的软件包版本号'''
    # TODO 需要判断是否需要更新osplugin包
    for i in data['softpkg']:
        if i['scenario'] == 'default':
            for j in i['data']:
                if j['__product'] == 'unc':
                    j['version'] = version
        elif i['scenario'] == 'china':
            for j in i['data']:
                if j['__product'] == 'unc':
                    j['version'] = chs_version

    '''6、修改金字塔的归档cmc路径'''
    for i in data['cmcArchive']:
        if i['name'] == 'default':
            i['version'] = archive_cmc_version
            i['warehouse'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M")
            print(i['warehouse'])
        elif i['name'] == 'china':
            i['version'] = archive_chs_cmc_version
            i['warehouse'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M")

    '''7、修改补丁基线版本'''
    '''有前补丁的不需要修改基线信息！'''

    '''8、修改前补丁配置'''
    data['patch']['prePatchVersion'] = pre_arti_branch
    for i in data['patch']['prePatchArti']:
        if '__product' == 'unc' and pre_arti_branch.replace('/', '-') in i['artifactId']:
            i['artifactId'].replace(pre_arti_branch.replace('/', '-'), '')
            i['version'].replace(i['version'], pre_arti_version)
        elif '__product' == 'unc' and i['artifactId'] == i['name']:
            i['version'] = pre_arti_version

    with open('./config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return resp


def mod_b_gt_info(basebranch):
    resp = get_gt_info(branch).json()
    data = resp['config']

    '''
    修改从B版本拉出的金字塔配置
    '''

    '''1、修改version页签'''
    for i in data['product']:
        if i['scenario'] == 'default':
            i['appVersion'] = version
            i['interfaceId'] = version
            i['data']['appVersion'] = version
            i['data']['interfaceId'] = version

        if i['scenario'] == 'china':
            i['appVersion'] = chs_version
            i['interfaceId'] = version
            i['data']['appVersion'] = version
            i['data']['interfaceId'] = version
            i['modOriginFromPatch'] = '20.5.2.10'
            i['modOriginFromBase'] = '20.5.2'

    for i in data['artiArchive']:
        if i['scenario'] == 'default':
            i['version'] = version + '-SNAPSHOT'
        if i['scenario'] == 'china':
            i['version'] = chs_version + '-SNAPSHOT'

    '''2、修改金字塔repo页签'''
    for i in data['repo']:
        if i['__product'] == 'unc':
            i['flag'] = branch

    '''3、修改金字塔的arti页签'''
    for j in data['arti']:
        if j['__product'] == 'unc':
            j['artifactId'] = branch.replace('/', '-') + '-' + j['name']
            j['version'] = version

    '''4、修改金字塔的cmc页签'''
    for i in data['cmc']:
        if i['name'] == 'ServiceFabric 30':
            i['version'] = sf_cmc_version

    '''5、修改金字塔的软件包版本号'''
    for i in data['softpkg']:
        if i['scenario'] == 'default':
            for j in i['data']:
                if j['__product'] == 'unc':
                    j['version'] = version
        elif i['scenario'] == 'china':
            for j in i['data']:
                if j['__product'] == 'unc':
                    j['version'] = chs_version

    '''6、修改金字塔的归档cmc路径'''
    for i in data['cmcArchive']:
        if i['name'] == 'default':
            i['version'] = archive_cmc_version
            i['warehouse'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M")
            print(i['warehouse'])
        elif i['name'] == 'china':
            i['version'] = archive_chs_cmc_version
            i['warehouse'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M")

    '''7、修改补丁基线版本'''
    data['patch']['baseVersion'] = base_branch
    # TODO 修改补丁基线的信息，需要新加arti信息
    for i in data['patch']['baseArti']:
        if '__product' == 'unc' and base_branch.replace('/', '-') in i['artifactId']:
            i['artifactId'].replace(base_branch.replace('/', '-'), '')
            i['version'].replace(i['version'], base_arti_version)

    '''8、修改前补丁配置'''
    # TODO 不用修改前arti的信息，没有前补丁
    data['patch']['prePatchVersion'] = pre_arti_branch
    for i in data['patch']['prePatchArti']:
        if '__product' == 'unc' and pre_arti_branch.replace('/', '-') in i['artifactId']:
            i['artifactId'].replace(pre_arti_branch.replace('/', '-'), '')
            i['version'].replace(i['version'], base_arti_version)

    with open('./config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)


def submit_info():
    sub_url = "http://goldentower.inhuawei.com/api/v2/config/ci"
    Headers = {'Content-Type': 'application/json'}
    data = mod_pre_gt_info(branch)
    request_data = {
        "group": "unc",
        "configName": branch,
        "config": data["config"],
        "commitMsg": "modify",
        "author": "wwx875840"
    }
    resp = requests.post(url=sub_url, json=request_data, headers=Headers)
    print(resp.text)


def main():
    submit_info()


if __name__ == '__main__':
    main()
