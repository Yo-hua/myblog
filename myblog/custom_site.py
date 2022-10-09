from django.contrib.admin import AdminSite


# 实现自定义的管理后台

class CustomSite(AdminSite):
    site_header = 'myblog'
    site_title = 'Blog management background'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')
