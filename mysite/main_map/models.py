from django.db import models


class City(models.Model):
    x =  models.FloatField(db_index=True, blank=True, null=True)
    y =  models.FloatField(db_index=True, blank=True, null=True)
    lon = models.FloatField(db_index=True, blank=True, null=True)
    lat = models.FloatField(db_index=True, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    source_id = models.TextField(blank=True, null=True)
    source_name = models.TextField(blank=True, null=True)
    
class AlcoStopper(models.Model):
    x =  models.FloatField(db_index=True, blank=True, null=True)
    y =  models.FloatField(db_index=True, blank=True, null=True)
    lat =  models.FloatField(db_index=True, blank=True, null=True)
    lon =  models.FloatField(db_index=True, blank=True, null=True)
    chain_name = models.TextField(blank=True, null=True)
    nat_class = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    source_id = models.TextField(blank=True, null=True)
    source_name = models.TextField(blank=True, null=True)
    cafe = models.NullBooleanField(blank=True, null=True)
    
    
    
class PredictedSquare(models.Model):
    x =  models.FloatField(db_index=True, blank=True, null=True)
    y =  models.FloatField(db_index=True, blank=True, null=True)
    revenue_pred_model1 =  models.FloatField(blank=True, null=True)
    revenue_pred_model2 =  models.FloatField(blank=True, null=True)
    machine_features = models.TextField(blank=True, null=True)
    

class TimePolygons(models.Model):
    x =  models.FloatField(db_index=True, blank=True, null=True)
    y =  models.FloatField(db_index=True, blank=True, null=True)
    time =  models.FloatField(blank=True, null=True)
    geojson =  models.TextField(blank=True, null=True)
    geojson_smoothed =  models.TextField(blank=True, null=True)
    cafe =  models.NullBooleanField(blank=True, null=True)  
    alco_stopper_id = models.IntegerField(blank=True, null=True)
    
class TimePolygonsUnion(models.Model):
    x =  models.FloatField(db_index=True, blank=True, null=True)
    y =  models.FloatField(db_index=True, blank=True, null=True)
    time =  models.FloatField(db_index=True, blank=True, null=True)
    geojson =  models.TextField(blank=True, null=True)
    geojson_smoothed =  models.TextField(blank=True, null=True)
    cafe =  models.NullBooleanField(blank=True, null=True)  
    alco_stopper_id = models.IntegerField(blank=True, null=True)
    
class TimeSquare(models.Model):
    x =  models.FloatField(db_index=True, blank=True, null=True)
    y =  models.FloatField(db_index=True, blank=True, null=True)
    driving =  models.FloatField(blank=True, null=True)
    foot =  models.FloatField(blank=True, null=True)    
    
class Distance(models.Model):
    source_id1 = models.TextField(db_index=True, blank=True, null=True)
    source_name1 = models.TextField(db_index=True, blank=True, null=True)
    
    source_id2 = models.TextField(db_index=True, blank=True, null=True)
    source_name2 = models.TextField(db_index=True, blank=True, null=True)
    nat_class =  models.TextField(db_index=True, blank=True, null=True)
    euclid_distance = models.FloatField(blank=True, null=True)
    euclid_distance_metro = models.FloatField(blank=True, null=True)
    euclid_distance_city = models.FloatField(blank=True, null=True)

class DistanceTemp(Distance):
    pass

class SalePoint(models.Model):
    x =  models.FloatField(blank=True, null=True)
    y =  models.FloatField(blank=True, null=True)
    cann = models.TextField(blank=True, null=True)
    comp = models.TextField(blank=True, null=True)
    revenue_pred_model1 =  models.FloatField(blank=True, null=True)
    revenue_pred_model2 =  models.FloatField(blank=True, null=True)
    machine_features = models.TextField(blank=True, null=True)
    isocrone_coords = models.TextField(blank=True, null=True)
    isocrone_times = models.TextField(blank=True, null=True)
    
    
    
class OperSquare(models.Model):
    if_home = models.NullBooleanField(db_index=True, blank=True, null=True)
    male = models.NullBooleanField(db_index=True, blank=True, null=True)
    age = models.FloatField(db_index=True, blank=True, null=True)
    income = models.FloatField(db_index=True, blank=True, null=True)
    users = models.FloatField(blank=True, null=True)
    x =  models.FloatField(db_index=True, blank=True, null=True)
    y =  models.FloatField(db_index=True, blank=True, null=True)
    source_id = models.TextField(blank=True, null=True)

class LineModel(models.Model):
    lat0 = models.FloatField(blank=True, null=True)
    lon0 = models.FloatField(blank=True, null=True)
    lat1 = models.FloatField(blank=True, null=True)
    lon1 = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    n_parts = models.FloatField(blank=True, null=True)
    
    mode = models.CharField(default='', max_length=30)
    att = models.CharField(default='', max_length=30)
    

class RawLine(models.Model):
    address = models.TextField(blank=True, null=True)
    
    lat0 = models.FloatField(blank=True, null=True)
    lon0 = models.FloatField(blank=True, null=True)
    lat1 = models.FloatField(blank=True, null=True)
    lon1 = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    mode = models.CharField(default='', max_length=30)
    att = models.CharField(default='', max_length=30)

class PolygonModel(models.Model):
    
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    
    points = models.TextField(blank=True, null=True)
    eng_name = models.TextField(blank=True, null=True)
    nat_name = models.TextField(blank=True, null=True)
    scale = models.TextField(blank=True, null=True)
    flat_num = models.FloatField(blank=True, null=True)
    sale_price = models.FloatField(blank=True, null=True)
    
    nat_class_stat = models.TextField(blank=True, null=True)


class AbstractObject(models.Model):
    
    class Meta:
        abstract = True
        
    lat = models.FloatField(db_index=True, blank=True, null=True)
    lon = models.FloatField(db_index=True, blank=True, null=True)
    
    x = models.FloatField(db_index=True, blank=True, null=True)
    y = models.FloatField(db_index=True, blank=True, null=True)
    
    address = models.TextField(blank=True, null=True)
    source_id = models.TextField(blank=True, null=True)
    source_name = models.TextField(blank=True, null=True)


class Organization(AbstractObject):
    pass

class OrganizationNatClass(AbstractObject):
    chain_name = models.TextField(db_index=True, blank=True, null=True)
    nat_class = models.TextField(db_index=True, blank=True, null=True)
    
class Workplace(AbstractObject):
    chain_name = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    
class House(AbstractObject):
    
    square = models.FloatField(blank=True, null=True)
    sq_avg = models.FloatField(blank=True, null=True)
    flat_num = models.FloatField(blank=True, null=True)
    sale_price = models.FloatField(blank=True, null=True)
    nearest_nat_classes_euclid = models.TextField(blank=True, null=True)
    nearest_nat_classes_metro_euclid = models.TextField(blank=True, null=True)

# class Office(AbstractObject):
#     square = models.TextField(blank=True, null=True)
#     n_lines =  models.IntegerField(blank=True, null=True)
    
class MetroStation(AbstractObject):
    
    station_name = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    
class Metro(AbstractObject):
    
    station_name = models.TextField(blank=True, null=True)
    exit_name = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    
class GroundStop(AbstractObject):
    stop_name = models.TextField(blank=True, null=True)
    n_lines =  models.IntegerField(blank=True, null=True)
    