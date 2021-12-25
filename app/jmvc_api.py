from fastapi import FastAPI,APIRouter
import uvicorn
from typing import Optional
from influxdb import InfluxDBClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# import array 
from datetime import datetime, time
from dateutil import tz, parser
app = FastAPI()
origins = ["*"]
smp_gol1=1
smp_small_bus=1.3
smp_big_bus=1.5
smp_gol2=1.3
smp_gol345=2
Phf=0.06
beban_ruas=90479

# lajur_aktual=2
# kapasitas_dasar=2300
# Fcw=1.02
# Fcsp=1
capacity=8147*2
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Indonesia/Jakarta')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#ada database local computer localhost, database jmvc
client = InfluxDBClient(host='20.10.20.48',
                    port=8086,
                    username='',
                    password='',
                    database='jmvc')

def minutes():
    array_minutes =list()
    query_minutes = client.query('SELECT sum(*) FROM "counter_data" where time> now() - 10m group by time(1m) ')
    for measurement in query_minutes.get_points(measurement='counter_data'):
        x_minutes=measurement['time'].split(":")[0][0:10]+" "+measurement['time'].split(":")[0][11:13]+':'+measurement['time'].split(":")[1]+':'+measurement["time"].split(":")[2]
        utc = datetime.strptime(x_minutes[0:19], '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        string_minutes=local.strftime('%Y-%m-%d %H:%M:%S')[0:19]
        if measurement["sum_speed_down"] is not None:
            speed_down_converted=round(measurement["sum_speed_down"], 2)
        else:
            speed_down_converted=None
        if measurement["sum_speed_up"] is not None:
            speed_up_converted=round(measurement["sum_speed_up"], 2)
        else:
            speed_up_converted=None
        dict_minutes={"time":string_minutes,
            "sum_bus_l_down": measurement["sum_bus(l)_down"],
            "sum_bus_l_up": measurement["sum_bus(l)_up"],
            "sum_bus_s_down": measurement["sum_bus(s)_down"],
            "sum_bus_s_up": measurement["sum_bus(s)_up"],
            "sum_car_down": measurement["sum_car_down"],
            "sum_car_up": measurement["sum_car_up"],
            "sum_speed_down":speed_down_converted,
            "sum_speed_up":speed_up_converted,
            "sum_truck_l_down": measurement["sum_truck(l)_down"],
            "sum_truck_l_up": measurement["sum_truck(l)_up"],
            "sum_truck_m_down": measurement["sum_truck(m)_down"],
            "sum_truck_m_up": measurement["sum_truck(m)_up"],
            "sum_truck_s_down": measurement["sum_truck(s)_down"],
            "sum_truck_s_up": measurement["sum_truck(s)_up"],
            "sum_truck_xl_down": measurement["sum_truck(xl)_down"],
            "sum_truck_xl_up": measurement["sum_truck(xl)_up"]
        }
        array_minutes.append(dict_minutes)
    array_minutes.pop(0) 
    return array_minutes

def hours():
    array_hours =list()
    query_hours=client.query('SELECT mean("speed_down"),mean("speed_up"),sum(*) FROM "counter_data" where time> now()-10h group by time(1h)')
    for measurement in query_hours.get_points(measurement='counter_data'):
        x_hours=measurement['time'].split(":")[0][0:10]+" "+measurement['time'].split(":")[0][11:13]+':'+measurement['time'].split(":")[1]+':'+measurement["time"].split(":")[2]
        utc = datetime.strptime(x_hours[0:19], '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        string_hours=local.strftime('%Y-%m-%d %H:%M:%S')[0:19]
        if measurement['mean'] is not None:
            speed_down_converted=round(measurement["mean"], 2)
        else:
            speed_down_converted=None
        if measurement['mean_1'] is not None:
            speed_up_converted=round(measurement["mean_1"], 2)
        else:
            speed_up_converted=None
        dict_hours={"time":string_hours,
            "sum_bus_l_down": measurement["sum_bus(l)_down"],
            "sum_bus_l_up": measurement["sum_bus(l)_up"],
            "sum_bus_s_down": measurement["sum_bus(s)_down"],
            "sum_bus_s_up": measurement["sum_bus(s)_up"],
            "sum_car_down": measurement["sum_car_down"],
            "sum_car_up": measurement["sum_car_up"],
            "sum_speed_down":speed_down_converted,
            "sum_speed_up":speed_up_converted,
            "sum_truck_l_down": measurement["sum_truck(l)_down"],
            "sum_truck_l_up": measurement["sum_truck(l)_up"],
            "sum_truck_m_down": measurement["sum_truck(m)_down"],
            "sum_truck_m_up": measurement["sum_truck(m)_up"],
            "sum_truck_s_down": measurement["sum_truck(s)_down"],
            "sum_truck_s_up": measurement["sum_truck(s)_up"],
            "sum_truck_xl_down": measurement["sum_truck(xl)_down"],
            "sum_truck_xl_up": measurement["sum_truck(xl)_up"]
        }
        array_hours.append(dict_hours)

    array_hours.pop(0)
    return array_hours

def days():
    array_days=list()
    query_days=client.query('SELECT mean("speed_down"),mean("speed_up"),sum(*) FROM "counter_data" where time> now()-10d group by time(1d)')
    for measurement in query_days.get_points(measurement='counter_data'):
        x_days=measurement['time'].split(":")[0][0:10]+" "+measurement['time'].split(":")[0][11:13]+':'+measurement['time'].split(":")[1]+':'+measurement["time"].split(":")[2]
        utc = datetime.strptime(x_days[0:19], '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)
        string_days=local.strftime('%Y-%m-%d %H:%M:%S')[0:19]       
        if measurement['mean'] is not None:
            speed_down_converted=round(measurement["mean"], 2)
        else:
            speed_down_converted=None
        if measurement['mean_1'] is not None:
            speed_up_converted=round(measurement["mean_1"], 2)
        else:
            speed_up_converted=None
        dict_days={"time":string_days,
            "sum_bus_l_down": measurement["sum_bus(l)_down"],
            "sum_bus_l_up": measurement["sum_bus(l)_up"],
            "sum_bus_s_down": measurement["sum_bus(s)_down"],
            "sum_bus_s_up": measurement["sum_bus(s)_up"],
            "sum_car_down": measurement["sum_car_down"],
            "sum_car_up": measurement["sum_car_up"],
            "sum_speed_down":speed_down_converted,
            "sum_speed_up":speed_up_converted,
            "sum_truck_l_down": measurement["sum_truck(l)_down"],
            "sum_truck_l_up": measurement["sum_truck(l)_up"],
            "sum_truck_m_down": measurement["sum_truck(m)_down"],
            "sum_truck_m_up": measurement["sum_truck(m)_up"],
            "sum_truck_s_down": measurement["sum_truck(s)_down"],
            "sum_truck_s_up": measurement["sum_truck(s)_up"],
            "sum_truck_xl_down": measurement["sum_truck(xl)_down"],
            "sum_truck_xl_up": measurement["sum_truck(xl)_up"]
        }
        array_days.append(dict_days)

    array_days.pop(0)
    return array_days

def vc_ratio_minutes():
    vehicle_total=minutes()
    vehicle_total=vehicle_total[9]

    #lajur up
    v_up_total=vehicle_total['sum_bus_l_up']+vehicle_total['sum_bus_s_up']+vehicle_total['sum_car_up']+vehicle_total['sum_truck_l_up']+vehicle_total['sum_truck_s_up']+vehicle_total['sum_truck_m_up']+vehicle_total['sum_truck_xl_up']
    presentase_bus_l_up=round((vehicle_total['sum_bus_l_up']/v_up_total)*100,2)
    presentase_bus_s_up=round((vehicle_total['sum_bus_s_up']/v_up_total)*100,2)
    presentase_car_up=round((vehicle_total['sum_car_up']/v_up_total)*100,2)
    presentase_truck_l_up=round((vehicle_total['sum_truck_l_up']/v_up_total)*100,2)
    presentase_truck_s_up=round((vehicle_total['sum_truck_s_up']/v_up_total)*100,2)
    presentase_truck_m_up=round((vehicle_total['sum_truck_m_up']/v_up_total)*100,2)
    presentase_truck_xl_up=round((vehicle_total['sum_truck_xl_up']/v_up_total)*100,2)
    v_bus_l_up=beban_ruas*Phf*(presentase_bus_l_up/100)*smp_big_bus
    v_bus_s_up=beban_ruas*Phf*(presentase_bus_s_up/100)*smp_small_bus
    v_car_up=beban_ruas*Phf*(presentase_car_up/100)*smp_gol1
    v_truck_xl_up=beban_ruas*Phf*(presentase_truck_xl_up/100)*smp_gol345
    v_truck_l_up=beban_ruas*Phf*(presentase_truck_l_up/100)*smp_gol345
    v_truck_m_up=beban_ruas*Phf*(presentase_truck_m_up/100)*smp_gol2
    v_truck_s_up=beban_ruas*Phf*(presentase_truck_s_up/100)*smp_gol2
    v_total_up=v_bus_l_up+v_bus_s_up+v_car_up+v_truck_xl_up+v_truck_l_up+v_truck_m_up+v_truck_s_up
    vc_ratio_up=round((v_total_up/capacity),2) 

    #lajur down
    v_down_total=vehicle_total['sum_bus_l_down']+vehicle_total['sum_bus_s_down']+vehicle_total['sum_car_down']+vehicle_total['sum_truck_l_down']+vehicle_total['sum_truck_s_down']+vehicle_total['sum_truck_m_down']+vehicle_total['sum_truck_xl_down']
    presentase_bus_l_down=round((vehicle_total['sum_bus_l_down']/v_down_total)*100,2)
    presentase_bus_s_down=round((vehicle_total['sum_bus_s_down']/v_down_total)*100,2)
    presentase_car_down=round((vehicle_total['sum_car_down']/v_down_total)*100,2)
    presentase_truck_l_down=round((vehicle_total['sum_truck_l_down']/v_down_total)*100,2)
    presentase_truck_s_down=round((vehicle_total['sum_truck_s_down']/v_down_total)*100,2)
    presentase_truck_m_down=round((vehicle_total['sum_truck_m_down']/v_down_total)*100,2)
    presentase_truck_xl_down=round((vehicle_total['sum_truck_xl_down']/v_down_total)*100,2)
    v_bus_l_down=beban_ruas*Phf*(presentase_bus_l_down/100)*smp_big_bus
    v_bus_s_down=beban_ruas*Phf*(presentase_bus_s_down/100)*smp_small_bus
    v_car_down=beban_ruas*Phf*(presentase_car_down/100)*smp_gol1
    v_truck_xl_down=beban_ruas*Phf*(presentase_truck_xl_down/100)*smp_gol345
    v_truck_l_down=beban_ruas*Phf*(presentase_truck_l_down/100)*smp_gol345
    v_truck_m_down=beban_ruas*Phf*(presentase_truck_m_down/100)*smp_gol2
    v_truck_s_down=beban_ruas*Phf*(presentase_truck_s_down/100)*smp_gol2
    v_total_down=v_bus_l_down+v_bus_s_down+v_car_down+v_truck_xl_down+v_truck_l_down+v_truck_m_down+v_truck_s_down
    vc_ratio_down=round((v_total_down/capacity),2)

    json_vc_ratio = {"vc_ratio_up":vc_ratio_up,"presentase_bus_l_up":presentase_bus_l_up,"presentase_bus_s_up":presentase_bus_s_up,"presentase_car_up":presentase_car_up,
    "presentase_truck_l_up":presentase_truck_l_up,"presentase_truck_s_up":presentase_truck_s_up,"presentase_truck_m_up":presentase_truck_m_up,
    "presentase_truck_xl_up":presentase_truck_xl_up,"vc_ratio_down":vc_ratio_down,"presentase_bus_l_down":presentase_bus_l_down,
    "presentase_bus_s_down":presentase_bus_s_down,"presentase_car_down":presentase_car_down,"presentase_truck_l_down":presentase_truck_l_down,
    "presentase_truck_s_down":presentase_truck_s_down,"presentase_truck_m_down":presentase_truck_m_down,"presentase_truck_xl_down":presentase_truck_xl_down,}
    
    return json_vc_ratio

def vc_ratio_hours():
    vehicle_total=hours()
    vehicle_total=vehicle_total[9]
    #lajur up
    v_up_total=vehicle_total['sum_bus_l_up']+vehicle_total['sum_bus_s_up']+vehicle_total['sum_car_up']+vehicle_total['sum_truck_l_up']+vehicle_total['sum_truck_s_up']+vehicle_total['sum_truck_m_up']+vehicle_total['sum_truck_xl_up']
    presentase_bus_l_up=round((vehicle_total['sum_bus_l_up']/v_up_total)*100,2)
    presentase_bus_s_up=round((vehicle_total['sum_bus_s_up']/v_up_total)*100,2)
    presentase_car_up=round((vehicle_total['sum_car_up']/v_up_total)*100,2)
    presentase_truck_l_up=round((vehicle_total['sum_truck_l_up']/v_up_total)*100,2)
    presentase_truck_s_up=round((vehicle_total['sum_truck_s_up']/v_up_total)*100,2)
    presentase_truck_m_up=round((vehicle_total['sum_truck_m_up']/v_up_total)*100,2)
    presentase_truck_xl_up=round((vehicle_total['sum_truck_xl_up']/v_up_total)*100,2)
    v_bus_l_up=beban_ruas*Phf*(presentase_bus_l_up/100)*smp_big_bus
    v_bus_s_up=beban_ruas*Phf*(presentase_bus_s_up/100)*smp_small_bus
    v_car_up=beban_ruas*Phf*(presentase_car_up/100)*smp_gol1
    v_truck_xl_up=beban_ruas*Phf*(presentase_truck_xl_up/100)*smp_gol345
    v_truck_l_up=beban_ruas*Phf*(presentase_truck_l_up/100)*smp_gol345
    v_truck_m_up=beban_ruas*Phf*(presentase_truck_m_up/100)*smp_gol2
    v_truck_s_up=beban_ruas*Phf*(presentase_truck_s_up/100)*smp_gol2
    v_total_up=v_bus_l_up+v_bus_s_up+v_car_up+v_truck_xl_up+v_truck_l_up+v_truck_m_up+v_truck_s_up
    vc_ratio_up=round((v_total_up/capacity),2) 

    #lajur down
    v_down_total=vehicle_total['sum_bus_l_down']+vehicle_total['sum_bus_s_down']+vehicle_total['sum_car_down']+vehicle_total['sum_truck_l_down']+vehicle_total['sum_truck_s_down']+vehicle_total['sum_truck_m_down']+vehicle_total['sum_truck_xl_down']
    presentase_bus_l_down=round((vehicle_total['sum_bus_l_down']/v_down_total)*100,2)
    presentase_bus_s_down=round((vehicle_total['sum_bus_s_down']/v_down_total)*100,2)
    presentase_car_down=round((vehicle_total['sum_car_down']/v_down_total)*100,2)
    presentase_truck_l_down=round((vehicle_total['sum_truck_l_down']/v_down_total)*100,2)
    presentase_truck_s_down=round((vehicle_total['sum_truck_s_down']/v_down_total)*100,2)
    presentase_truck_m_down=round((vehicle_total['sum_truck_m_down']/v_down_total)*100,2)
    presentase_truck_xl_down=round((vehicle_total['sum_truck_xl_down']/v_down_total)*100,2)
    v_bus_l_down=beban_ruas*Phf*(presentase_bus_l_down/100)*smp_big_bus
    v_bus_s_down=beban_ruas*Phf*(presentase_bus_s_down/100)*smp_small_bus
    v_car_down=beban_ruas*Phf*(presentase_car_down/100)*smp_gol1
    v_truck_xl_down=beban_ruas*Phf*(presentase_truck_xl_down/100)*smp_gol345
    v_truck_l_down=beban_ruas*Phf*(presentase_truck_l_down/100)*smp_gol345
    v_truck_m_down=beban_ruas*Phf*(presentase_truck_m_down/100)*smp_gol2
    v_truck_s_down=beban_ruas*Phf*(presentase_truck_s_down/100)*smp_gol2
    v_total_down=v_bus_l_down+v_bus_s_down+v_car_down+v_truck_xl_down+v_truck_l_down+v_truck_m_down+v_truck_s_down
    vc_ratio_down=round((v_total_down/capacity),2) 

    json_vc_ratio = {"vc_ratio_up":vc_ratio_up,"presentase_bus_l_up":presentase_bus_l_up,"presentase_bus_s_up":presentase_bus_s_up,"presentase_car_up":presentase_car_up,
    "presentase_truck_l_up":presentase_truck_l_up,"presentase_truck_s_up":presentase_truck_s_up,"presentase_truck_m_up":presentase_truck_m_up,
    "presentase_truck_xl_up":presentase_truck_xl_up,"vc_ratio_down":vc_ratio_down,"presentase_bus_l_down":presentase_bus_l_down,
    "presentase_bus_s_down":presentase_bus_s_down,"presentase_car_down":presentase_car_down,"presentase_truck_l_down":presentase_truck_l_down,
    "presentase_truck_s_down":presentase_truck_s_down,"presentase_truck_m_down":presentase_truck_m_down,"presentase_truck_xl_down":presentase_truck_xl_down,}
    
    return json_vc_ratio

def vc_ratio_days():
    vehicle_total=days()
    vehicle_total=vehicle_total[9]

    #lajur up
    v_up_total=vehicle_total['sum_bus_l_up']+vehicle_total['sum_bus_s_up']+vehicle_total['sum_car_up']+vehicle_total['sum_truck_l_up']+vehicle_total['sum_truck_s_up']+vehicle_total['sum_truck_m_up']+vehicle_total['sum_truck_xl_up']
    presentase_bus_l_up=round((vehicle_total['sum_bus_l_up']/v_up_total)*100,2)
    presentase_bus_s_up=round((vehicle_total['sum_bus_s_up']/v_up_total)*100,2)
    presentase_car_up=round((vehicle_total['sum_car_up']/v_up_total)*100,2)
    presentase_truck_l_up=round((vehicle_total['sum_truck_l_up']/v_up_total)*100,2)
    presentase_truck_s_up=round((vehicle_total['sum_truck_s_up']/v_up_total)*100,2)
    presentase_truck_m_up=round((vehicle_total['sum_truck_m_up']/v_up_total)*100,2)
    presentase_truck_xl_up=round((vehicle_total['sum_truck_xl_up']/v_up_total)*100,2)
    v_bus_l_up=beban_ruas*Phf*(presentase_bus_l_up/100)*smp_big_bus
    v_bus_s_up=beban_ruas*Phf*(presentase_bus_s_up/100)*smp_small_bus
    v_car_up=beban_ruas*Phf*(presentase_car_up/100)*smp_gol1
    v_truck_xl_up=beban_ruas*Phf*(presentase_truck_xl_up/100)*smp_gol345
    v_truck_l_up=beban_ruas*Phf*(presentase_truck_l_up/100)*smp_gol345
    v_truck_m_up=beban_ruas*Phf*(presentase_truck_m_up/100)*smp_gol2
    v_truck_s_up=beban_ruas*Phf*(presentase_truck_s_up/100)*smp_gol2
    v_total_up=v_bus_l_up+v_bus_s_up+v_car_up+v_truck_xl_up+v_truck_l_up+v_truck_m_up+v_truck_s_up
    vc_ratio_up=round((v_total_up/capacity),2) 

    #lajur down
    v_down_total=vehicle_total['sum_bus_l_down']+vehicle_total['sum_bus_s_down']+vehicle_total['sum_car_down']+vehicle_total['sum_truck_l_down']+vehicle_total['sum_truck_s_down']+vehicle_total['sum_truck_m_down']+vehicle_total['sum_truck_xl_down']
    presentase_bus_l_down=round((vehicle_total['sum_bus_l_down']/v_down_total)*100,2)
    presentase_bus_s_down=round((vehicle_total['sum_bus_s_down']/v_down_total)*100,2)
    presentase_car_down=round((vehicle_total['sum_car_down']/v_down_total)*100,2)
    presentase_truck_l_down=round((vehicle_total['sum_truck_l_down']/v_down_total)*100,2)
    presentase_truck_s_down=round((vehicle_total['sum_truck_s_down']/v_down_total)*100,2)
    presentase_truck_m_down=round((vehicle_total['sum_truck_m_down']/v_down_total)*100,2)
    presentase_truck_xl_down=round((vehicle_total['sum_truck_xl_down']/v_down_total)*100,2)
    v_bus_l_down=beban_ruas*Phf*(presentase_bus_l_down/100)*smp_big_bus
    v_bus_s_down=beban_ruas*Phf*(presentase_bus_s_down/100)*smp_small_bus
    v_car_down=beban_ruas*Phf*(presentase_car_down/100)*smp_gol1
    v_truck_xl_down=beban_ruas*Phf*(presentase_truck_xl_down/100)*smp_gol345
    v_truck_l_down=beban_ruas*Phf*(presentase_truck_l_down/100)*smp_gol345
    v_truck_m_down=beban_ruas*Phf*(presentase_truck_m_down/100)*smp_gol2
    v_truck_s_down=beban_ruas*Phf*(presentase_truck_s_down/100)*smp_gol2
    v_total_down=v_bus_l_down+v_bus_s_down+v_car_down+v_truck_xl_down+v_truck_l_down+v_truck_m_down+v_truck_s_down
    vc_ratio_down=round((v_total_down/capacity),2) 

    json_vc_ratio = {"vc_ratio_up":vc_ratio_up,"presentase_bus_l_up":presentase_bus_l_up,"presentase_bus_s_up":presentase_bus_s_up,"presentase_car_up":presentase_car_up,
    "presentase_truck_l_up":presentase_truck_l_up,"presentase_truck_s_up":presentase_truck_s_up,"presentase_truck_m_up":presentase_truck_m_up,
    "presentase_truck_xl_up":presentase_truck_xl_up,"vc_ratio_down":vc_ratio_down,"presentase_bus_l_down":presentase_bus_l_down,
    "presentase_bus_s_down":presentase_bus_s_down,"presentase_car_down":presentase_car_down,"presentase_truck_l_down":presentase_truck_l_down,
    "presentase_truck_s_down":presentase_truck_s_down,"presentase_truck_m_down":presentase_truck_m_down,"presentase_truck_xl_down":presentase_truck_xl_down,}
    
    return json_vc_ratio



@app.get("/minutes/")
async def minute():
    return minutes()

@app.get("/hours/")
async def hour():
    return hours()

@app.get("/days/")
async def day():
    return days()

@app.get("/vc_ratio_minutes/")
async def vc_ratio_minute():
    return vc_ratio_minutes()

@app.get("/vc_ratio_hours/")
async def vc_ratio_hour():
    return vc_ratio_hours()

@app.get("/vc_ratio_days/")
async def vc_ratio_day():
    return vc_ratio_days()

if __name__ == "__main__":
    uvicorn.run("jmvc_api:app", host="192.168.99.27", port=8080,log_level="info",reload=True)