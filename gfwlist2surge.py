#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import base64
import getpass
import requests

__author__ = "ITXiaoPang"
__mtime__ = "2017/7/22"

curr_user = getpass.getuser()

gfwlist_url = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
gfwlist_file = "/tmp/gfwlist.txt"

surge_conf_path = f"/Users/{curr_user}/Library/Mobile Documents/iCloud~run~surge/Documents/"
surge_template = f"{surge_conf_path}Surge.conf"
surge_policy = "noProxy"
surge_flag_start = "//white_list_start"
surge_flag_end = "//white_list_end"
surge_gfw_conf = f"{surge_conf_path}Surge_GFW.conf"


if __name__ == "__main__":
    if not os.path.exists(surge_template):
        print(f"模板文件未找到：{surge_template}")
        exit()
    # Get GFW List
    print("开始读取GFW List")
    gfwlist_response = requests.get(gfwlist_url)
    if gfwlist_response.status_code == requests.codes.ok:
        print("读取GFW List成功")
        gfwlist_base64 = gfwlist_response.text
        print("开始解密GFW List")
        gfwlist = str(base64.urlsafe_b64decode(gfwlist_base64), encoding="utf-8")
        print("解密GFW List成功")
        print(f"将GFW List写入文件{gfwlist_file}")
        try:
            with open(gfwlist_file, mode="w", encoding="utf-8") as f_gfw_list:
                f_gfw_list.write(gfwlist)
        except IOError as ex:
            print(f"GFW List写入失败，错误：{ex}")
        else:
            print(f"GFW List写入成功:{gfwlist_file}")
    else:
        print(f"读取GFW List失败，尝试读取本地缓存:{gfwlist_file}。错误代码{gfwlist_response.status_code}")


    def format_url(rule, my_list):
        url = rule\
            .replace("@@", "")\
            .replace("|", "")\
            .replace("https://", "")\
            .replace("http://", "")\
            .replace(os.linesep, "")
        if url:
            if url not in my_list:
                my_list.append(url)


    if os.path.exists(gfwlist_file):
        print(f"读取文件{gfwlist_file}")
        try:
            white_list = []
            black_list = []
            with open(gfwlist_file, mode="r", encoding="utf-8") as f_gfw_list:

                for curr_rule in f_gfw_list.readlines():
                    if curr_rule:
                        if curr_rule.startswith("[") and curr_rule.endswith(f"]{os.linesep}"):
                            continue
                        elif curr_rule.startswith("!"):
                            continue
                        elif curr_rule.startswith("@@"):
                            format_url(curr_rule, white_list)
                        elif curr_rule.startswith("|"):
                            format_url(curr_rule, black_list)
                        else:
                            format_url(curr_rule, black_list)

            white_list_text = ""
            for curr_url in white_list:
                white_list_text += f"DOMAIN-SUFFIX,{curr_url},{surge_policy}{os.linesep}"

            white_list_text = "".join(
                [
                    surge_flag_start, os.linesep,
                    white_list_text, os.linesep,
                    surge_flag_end
                ]
            )

            if os.path.exists(surge_template):
                try:
                    print(f"读取模板{surge_template}")
                    with open(surge_template, mode="r", encoding="utf-8") as f_surge_template:
                        surge_template_text = f_surge_template.read()
                    comment = re.compile(f"{surge_flag_start}(.*?){surge_flag_end}", re.DOTALL)
                    if comment.findall(surge_template_text):
                        result, number = comment.subn(white_list_text, surge_template_text)
                        print(f"写入规则文件{surge_gfw_conf}")
                        with open(surge_gfw_conf, mode="w", encoding="utf-8") as f_surge_gfw_conf:
                            f_surge_gfw_conf.write(result)
                    else:
                        raise ModuleNotFoundError
                except IOError as ex:
                    print(f"规则写入失败，错误：{ex}")
                except ModuleNotFoundError:
                    print(f"未找到指定标记{surge_flag_start}和{surge_flag_end}")
                else:
                    print("规则写入成功")
        except IOError as ex:
            print(f"GFW List读取失败，错误：{ex}")
    else:
        print(f"文件{gfwlist_file}不存在。")
