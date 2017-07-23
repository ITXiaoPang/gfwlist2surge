# gfwlist2surge
## 按GFWList提供的白名单生成surge的配置文件
## 使用步骤
1. 安装Python3.6或以上版本（建议使用pyenv不会影响系统中原有Python的使用）。
2. 用文本编辑器（vi，sublime text等）打开gfwlist2surge.py文件。
3. 如果未使用iCloud同步Surge的配置文件，则修改surge_conf_path等号后面的路径为你自己实际存放配置文件的路径。
4. 将surge_policy等号后面的部分修改为你自己的策略，一般为DIRECT或nProxy或noProxy。
5. 准备一个Surge配置文件的模板，并命名为Surge.conf，放置在surge_conf_path路径中。
6. 在模板文件中的适当位置增加两行注释//white_list_start和//white_list_end（包含前面的//），白名单的规则将写入到模板的这两行注释中间。
7. 保存gfwlist2surge.py。
8. 运行gfwlist2surge.py。
9. 在surge_conf_path路径中生成带白名单的Surge配置文件Surge_GFW.conf。
10. 建议增加计划任务每天执行一次。