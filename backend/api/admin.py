"""
Django Admin Configuration for National Park Management System
"""
from django.contrib import admin
from . import models


@admin.register(models.FunctionalArea)
class FunctionalAreaAdmin(admin.ModelAdmin):
    list_display = ['area_id', 'area_name', 'area_type', 'area_size']
    list_filter = ['area_type']
    search_fields = ['area_name', 'area_id']


@admin.register(models.SystemUser)
class SystemUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'real_name', 'role_type', 'account_status', 'last_login_time']
    list_filter = ['role_type', 'account_status']
    search_fields = ['username', 'real_name', 'contact_phone']
    readonly_fields = ['create_time', 'last_login_time']


@admin.register(models.UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'login_time', 'last_activity_time', 'session_status']
    list_filter = ['session_status']
    search_fields = ['session_id', 'user__username']
    readonly_fields = ['login_time', 'last_activity_time']


@admin.register(models.Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ['species_id', 'chinese_name', 'latin_name', 'protection_level']
    list_filter = ['protection_level', 'kingdom', 'phylum']
    search_fields = ['chinese_name', 'latin_name', 'species_id']


@admin.register(models.Habitat)
class HabitatAdmin(admin.ModelAdmin):
    list_display = ['habitat_id', 'area_name', 'ecology_type', 'area_size', 'suitability_score']
    list_filter = ['ecology_type']
    search_fields = ['area_name', 'habitat_id']


@admin.register(models.MonitoringDevice)
class MonitoringDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'device_type', 'deployment_area', 'operation_status', 'installation_date']
    list_filter = ['operation_status', 'device_type']
    search_fields = ['device_id', 'device_type']


@admin.register(models.MonitoringRecord)
class MonitoringRecordAdmin(admin.ModelAdmin):
    list_display = ['record_id', 'species', 'monitoring_time', 'monitoring_method', 'data_status']
    list_filter = ['monitoring_method', 'data_status', 'monitoring_time']
    search_fields = ['record_id', 'species__chinese_name']
    date_hierarchy = 'monitoring_time'


@admin.register(models.MonitoringIndicator)
class MonitoringIndicatorAdmin(admin.ModelAdmin):
    list_display = ['indicator_id', 'indicator_name', 'unit', 'monitoring_frequency']
    list_filter = ['monitoring_frequency']
    search_fields = ['indicator_name', 'indicator_id']


@admin.register(models.EnvironmentalData)
class EnvironmentalDataAdmin(admin.ModelAdmin):
    list_display = ['data_id', 'indicator', 'collection_time', 'monitoring_value', 'data_quality']
    list_filter = ['data_quality', 'collection_time']
    search_fields = ['data_id', 'indicator__indicator_name']
    date_hierarchy = 'collection_time'


@admin.register(models.Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['visitor_id', 'visitor_name', 'contact_phone', 'entry_method', 'entry_time']
    list_filter = ['entry_method', 'entry_time']
    search_fields = ['visitor_name', 'id_card_number', 'contact_phone']


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_id', 'visitor', 'reservation_date', 'reservation_status', 'payment_status']
    list_filter = ['reservation_status', 'payment_status', 'reservation_date']
    search_fields = ['reservation_id', 'visitor__visitor_name']
    date_hierarchy = 'reservation_date'


@admin.register(models.TrafficControl)
class TrafficControlAdmin(admin.ModelAdmin):
    list_display = ['area', 'daily_capacity', 'current_visitor_count', 'warning_threshold', 'current_status']
    list_filter = ['current_status']
    search_fields = ['area__area_name']


@admin.register(models.LawEnforcer)
class LawEnforcerAdmin(admin.ModelAdmin):
    list_display = ['enforcer_id', 'enforcer_name', 'department', 'enforcement_authority', 'contact_phone']
    list_filter = ['department']
    search_fields = ['enforcer_name', 'enforcer_id', 'contact_phone']


@admin.register(models.IllegalBehavior)
class IllegalBehaviorAdmin(admin.ModelAdmin):
    list_display = ['record_id', 'behavior_type', 'occurrence_time', 'area', 'handling_status']
    list_filter = ['handling_status', 'behavior_type', 'occurrence_time']
    search_fields = ['record_id', 'behavior_type']
    date_hierarchy = 'occurrence_time'


@admin.register(models.EnforcementDispatch)
class EnforcementDispatchAdmin(admin.ModelAdmin):
    list_display = ['dispatch_id', 'record', 'enforcer', 'dispatch_time', 'dispatch_status']
    list_filter = ['dispatch_status', 'dispatch_time']
    search_fields = ['dispatch_id', 'enforcer__enforcer_name']
    date_hierarchy = 'dispatch_time'


@admin.register(models.ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ['project_id', 'project_name', 'principal', 'project_status', 'research_field']
    list_filter = ['project_status', 'research_field']
    search_fields = ['project_name', 'project_id', 'principal__real_name']


@admin.register(models.ResearchDataCollection)
class ResearchDataCollectionAdmin(admin.ModelAdmin):
    list_display = ['collection_id', 'project', 'collector', 'collection_time', 'data_source']
    list_filter = ['data_source', 'collection_time']
    search_fields = ['collection_id', 'project__project_name']
    date_hierarchy = 'collection_time'


@admin.register(models.ResearchAchievement)
class ResearchAchievementAdmin(admin.ModelAdmin):
    list_display = ['achievement_id', 'achievement_name', 'achievement_type', 'publish_date', 'share_permission']
    list_filter = ['achievement_type', 'share_permission', 'publish_date']
    search_fields = ['achievement_name', 'achievement_id']
    date_hierarchy = 'publish_date'
