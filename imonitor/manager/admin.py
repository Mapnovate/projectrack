from django.contrib import admin
from manager.models import *

# Register your models here.
class projectAdmin(admin.ModelAdmin):
    pass

class membershipAdmin(admin.ModelAdmin):
    pass

class departmentprojectsAdmin(admin.ModelAdmin):
    pass

class teamAdmin(admin.ModelAdmin):
    pass

class projectshipAdmin(admin.ModelAdmin):
    pass

class rolesAdmin(admin.ModelAdmin):
    pass

class teamshipAdmin(admin.ModelAdmin):
    pass

class tasktypeAdmin(admin.ModelAdmin):
    pass

class projecttypeAdmin(admin.ModelAdmin):
    pass

class departmentAdmin(admin.ModelAdmin):
    pass

class profileAdmin(admin.ModelAdmin):
    pass

class taskAdmin(admin.ModelAdmin):
    pass

class membersAdmin(admin.ModelAdmin):
    pass

admin.site.register(Projects, projectAdmin)
admin.site.register(Members, membersAdmin)
admin.site.register(Membership, membershipAdmin)
admin.site.register(Teams, teamAdmin)
admin.site.register(Tasks, taskAdmin)
admin.site.register(Departments, departmentAdmin)
#admin.site.register(Departmentprojects, departmentprojectsAdmin)
admin.site.register(Profile, profileAdmin)
admin.site.register(Projecttype, projecttypeAdmin)
admin.site.register(Teamship, teamshipAdmin)
admin.site.register(Tasktype, tasktypeAdmin)
admin.site.register(Roles, rolesAdmin)
admin.site.register(Projectship, projectshipAdmin)


