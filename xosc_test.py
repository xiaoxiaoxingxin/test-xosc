import pandas as pd
import os
from scenariogeneration import xosc, prettyprint, ScenarioGenerator
import pandas as pd
import re, copy
import openpyxl
import numpy as np

path_excel = r"C:\Users\99062\Desktop\sim_xosc\sim_test\excel_set\xosc_set.xlsx"

class TableParse:
    file_path = ""
    set_catalogs = []
    set_catalogs_directory = []
    set_logic_file = []
    set_scenario_graph_file = []
    set_pd_names = []
    set_pd_types = []
    set_pd_values = []
    set_en_so_name = []
    set_en_vehicle_name = []
    set_en_name = []
    set_en_name_value = []
    set_en_file_path = []
    set_en_car_type_r = []
    set_boxs = []
    set_axles = []
    set_axles_acc = []
    set_i_dynamics_shape_r = []
    set_i_dynamics_dimension_r = []
    set_i_sa_time_value = []
    set_i_sa_action_speed = []
    set_i_teleport_action = []
    ego_c_file = []
    ego_c_propert_name = []
    ego_c_propert_value = []
    target_c_catalog_name = []
    target_c_entry_name = []

    def __init__(self, f):
        self.file_path = f
        self.file_set = []

    def parse(self):
        self.table_catalog_locations()
        self.table_road_network()
        self.parameter_declaration()
        self.bounding()
        self.bounding_box()
        self.bounding_axle()
        self.bounding_axle_acc()
        self.actions_ints_speed_action()
        self.actions_ints_teleport_action()
        self.ego_controller()
        self.target_controller()

    def table_catalog_locations(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="CatalogLocations")
        self.set_catalogs = self.file_set["解析目录引用名称"]
        self.set_catalogs_directory = self.file_set["目录路径"]
        return self.set_catalogs, self.set_catalogs_directory

    def table_road_network(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="RoadNetwork")
        self.set_logic_file = self.file_set["LogicFile"]
        self.set_scenario_graph_file = self.file_set["SceneGraphFile"]
        return self.set_logic_file, self.set_scenario_graph_file

    def parameter_declaration(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="ParameterDeclaration")
        self.set_pd_names = self.file_set["name"]
        self.set_pd_types = self.file_set["parameterType"]
        self.set_pd_values = self.file_set["value"]
        for i in range(len(self.set_pd_types)):
            if self.set_pd_types[i] == "int":
                self.set_pd_types[i] = xosc.ParameterType.int
            elif self.set_pd_types[i] == "double":
                self.set_pd_types[i] = xosc.ParameterType.double
            elif self.set_pd_types[i] == "string":
                self.set_pd_types[i] = xosc.ParameterType.string
            elif self.set_pd_types[i] == "unsighedInt":
                self.set_pd_types[i] = xosc.ParameterType.unsighedInt
            elif self.set_pd_types[i] == "unsighedShort":
                self.set_pd_types[i] = xosc.ParameterType.unsighedShort
            elif self.set_pd_types[i] == "boolean":
                self.set_pd_types[i] = xosc.ParameterType.boolean
            elif self.set_pd_types[i] == "dateTime":
                self.set_pd_types[i] = xosc.ParameterType.dateTime
            else:
                print("参数类型错误")
        return self.set_pd_values, self.set_pd_types, self.set_pd_names

    def bounding(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="BoundingBox_Axles")
        self.set_en_so_name = self.file_set["ScenarioObject_name"]
        self.set_en_vehicle_name = self.file_set["Vehicle_name"]
        self.set_en_name = self.file_set["Property_name"]
        self.set_en_name_value = self.file_set["value"]
        self.set_en_file_path = self.file_set["filepath"]
        self.set_en_car_type = (self.file_set["car_type"])
        for i in range(len(self.set_en_car_type)):
            if self.set_en_car_type[i] == "car":
                self.set_en_car_type_r.append(xosc.VehicleCategory.car)
            elif self.set_en_car_type[i] == "van":
                self.set_en_car_type_r.append(xosc.VehicleCategory.van)
            elif self.set_en_car_type[i] == "truck":
                self.set_en_car_type_r.append(xosc.VehicleCategory.truck)
            elif self.set_en_car_type[i] == "trailer":
                self.set_en_car_type_r.append(xosc.VehicleCategory.trailer)
            elif self.set_en_car_type[i] == "semitrailer":
                self.set_en_car_type_r.append(xosc.VehicleCategory.semitrailer)
            elif self.set_en_car_type[i] == "bus":
                self.set_en_car_type_r.append(xosc.VehicleCategory.bus)
            elif self.set_en_car_type[i] == "motorbike":
                self.set_en_car_type_r.append(xosc.VehicleCategory.motorbike)
            elif self.set_en_car_type[i] == "bicycle":
                self.set_en_car_type_r.append(xosc.VehicleCategory.bicycle)
            elif self.set_en_car_type[i] == "train":
                self.set_en_car_type_r.append(xosc.VehicleCategory.train)
            elif self.set_en_car_type[i] == "tram":
                self.set_en_car_type_r.append(xosc.VehicleCategory.tram)
            else:
                print("车辆类型设置错误")
        return self.set_en_so_name, self.set_en_vehicle_name, self.set_en_name, self.set_en_name_value, self.set_en_file_path, self.set_en_car_type_r

    def bounding_box(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="BoundingBox_Axles", usecols=[5, 6, 7, 8, 9, 10])
        for i in range(len(self.file_set)):
            self.set_boxs.append([self.file_set["width"][i], self.file_set["length"][i], self.file_set["height"][i],
                                  self.file_set["x"][i], self.file_set["y"][i], self.file_set["z"][i]])
        return self.set_boxs

    def bounding_axle(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="BoundingBox_Axles", usecols=[11, 12, 13, 14, 15])
        for i in range(len(self.file_set)):
            self.set_axles.append([self.file_set["maxSteering"][i], self.file_set["wheelDiameter"][i],
                                   self.file_set["trackWidth"][i], self.file_set["positionX"][i],
                                   self.file_set["positionZ"][i]])
        return self.set_axles

    def bounding_axle_acc(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="BoundingBox_Axles", usecols=[16, 17, 18])
        for i in range(len(self.file_set)):
            self.set_axles_acc.append([self.file_set["maxSpeed"][i],
                                       self.file_set["maxDeceleration"][i], self.file_set["maxAcceleration"][i]])
        return self.set_axles_acc

    def actions_ints_speed_action(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="Actions_ints")
        self.set_i_dynamics_shape = self.file_set["dynamicsShape"]
        for i in range(len(self.set_i_dynamics_shape)):
            if self.set_i_dynamics_shape[i] == "step":
                self.set_i_dynamics_shape_r.append(xosc.DynamicsShapes.step)
            elif self.set_i_dynamics_shape[i] == "cubic":
                self.set_i_dynamics_shape_r.append(xosc.DynamicsShapes.cubic)
            elif self.set_i_dynamics_shape[i] == "sinusoidal":
                self.set_i_dynamics_shape_r.append(xosc.DynamicsShapes.sinusoidal)
            elif self.set_i_dynamics_shape[i] == "linear":
                self.set_i_dynamics_shape_r.append(xosc.DynamicsShapes.linear)
            else:
                print("参数类型错误")

        self.set_i_dynamics_dimension = self.file_set["dynamicsDimension"]
        for i in range(len(self.set_i_dynamics_dimension)):
            if self.set_i_dynamics_dimension[i] == "time":
                self.set_i_dynamics_dimension_r.append(xosc.DynamicsDimension.time)
            elif self.set_i_dynamics_dimension[i] == "rate":
                self.set_i_dynamics_dimension_r.append(xosc.DynamicsDimension.rate)
            elif self.set_i_dynamics_dimension[i] == "distance":
                self.set_i_dynamics_dimension_r.append(xosc.DynamicsDimension.distance)
            else:
                print("参数类型错误")

        self.set_i_sa_time_value = self.file_set["SpeedAction_time_value"]
        self.set_i_sa_action_speed = self.file_set["AbsoluteTargetSpeed"]
        return self.set_i_dynamics_shape_r, self.set_i_dynamics_dimension_r, self.set_i_sa_time_value, self.set_i_sa_action_speed

    def actions_ints_teleport_action(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="Actions_ints", usecols=[6, 4, 5, 7])
        for i in range(len(self.file_set)):
            self.set_i_teleport_action.append([self.file_set["s"][i], self.file_set["roadId"][i],
                                               self.file_set["laneId"][i], self.file_set["offset"][i]])
        return self.set_i_teleport_action

    def ego_controller(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="ego_controller")
        self.ego_c_file = self.file_set["ego_c_add_file"]
        self.ego_c_propert_name = self.file_set["ego_add_property"]
        self.ego_c_propert_value = self.file_set["value"]
        return self.ego_c_file, self.ego_c_propert_name, self.ego_c_propert_value

    def target_controller(self):
        self.file_set = pd.read_excel(self.file_path, sheet_name="target_controller")
        self.target_c_catalog_name = self.file_set["catalogname"]
        self.target_c_entry_name = self.file_set["entryname"]
        return self.target_c_catalog_name, self.target_c_entry_name
class TargetEvent:
    Event=[]
    def __init__(self,name,my_actionslist,my_triggerslist):
        self.name=name
        self.my_actionslist=my_actionslist
        self.my_triggerslist=my_triggerslist
    def GenerateEvents(self):
        if self.my_actionslist[0]=="RelativeLaneChangeAction" and self.my_triggerslist[0]=="AccelerationCondition":
            pass
        elif self.my_actionslist[0]=="RelativeLaneChangeAction" and self.my_triggerslist[0]=="LanePosition":
            pass


        

class Scenario(ScenarioGenerator):

    def __init__(self):
        super().__init__()
        self.open_scenario_version = 2

    def scenario(self, TableParse):
        # 创建解析目录引用 CatalogLocations
        # catalog.add_catalog("VehicleCatalog", "../xosc/Catalogs/Vehicles")
        catalog = xosc.Catalog()
        for i, j in zip(TableParse.set_catalogs, TableParse.set_catalogs_directory):
            catalog.add_catalog(i, j)

        # 加载地图，以及地图上的模型
        road = None
        for i, j in zip(TableParse.set_logic_file, TableParse.set_scenario_graph_file):
            road = xosc.RoadNetwork(roadfile=i, scenegraph=j)

        # 创建全局参数
        # paramdec.add_parameter(xosc.Parameter(ego_param_name, xosc.ParameterType.double, "10"))
        paramdec = xosc.ParameterDeclarations()
        for i, j, n in zip(TableParse.set_pd_names, TableParse.set_pd_types, TableParse.set_pd_values):
            paramdec.add_parameter(xosc.Parameter(i, j, n))

        # 创建场景车辆
        # 创建车辆的规格参数
        my_vehicle = []
        for i, j, n, m, k, o, p, l in zip(TableParse.set_en_vehicle_name, TableParse.set_en_car_type_r,
                                          TableParse.set_boxs, TableParse.set_axles,
                                          TableParse.set_axles_acc, TableParse.set_en_file_path,
                                          TableParse.set_en_name, TableParse.set_en_name_value):
            y = copy.deepcopy(m)
            y[3] = 0
            test = xosc.Vehicle(i, j, xosc.BoundingBox(*n), xosc.Axle(*m), xosc.Axle(*y), *k)
            test.add_property_file(o)
            test.add_property(p, str(l))
            my_vehicle.append(test)

        ## create entities
        # 创建场景实体对象
        entities = xosc.Entities()
        egoname = "Ego"
        targetname = "Target1"
        # 实体对象添加控制器参数或引用控制器，手动调整
        my_controller = []
        e_prop = xosc.Properties()
        for i, j in zip(TableParse.ego_c_propert_name, TableParse.ego_c_propert_value):
            e_prop.add_property(name=i, value=str(j))
        e_prop.add_file(TableParse.ego_c_file[0])
        e_cont = xosc.Controller("mycontroller", e_prop)
        targets_controller = []
        for i, j in zip(TableParse.target_c_catalog_name, TableParse.target_c_entry_name):
            targets_controller.append(xosc.CatalogReference(catalogname=i, entryname=j))
        my_controller = [e_cont] + targets_controller
        for i, j, n in zip(TableParse.set_en_so_name, my_vehicle, my_controller):
            entities.add_scenario_object(i, j, n)

        ### create init
        # 创建初始化段,只添加了一个初始速度，一个传送动作(相对参数可手动修改),一个控制器是否启用动作
        # 可以有很多。路径。轨迹。。。。
        init = xosc.Init()
        for i, j, n, o, k, m in zip(TableParse.set_i_dynamics_shape, TableParse.set_i_dynamics_dimension,
                                    TableParse.set_i_sa_time_value, TableParse.set_i_sa_action_speed,
                                    TableParse.set_i_teleport_action, TableParse.set_en_so_name):
            init.add_init_action(m, xosc.AbsoluteSpeedAction(o, xosc.TransitionDynamics(i, j, n)))
            init.add_init_action(m, xosc.TeleportAction(
                xosc.LanePosition(*k, xosc.Orientation(reference="relative", h="0", p="0", r="0"))))
            init.add_init_action(m, xosc.ActivateControllerAction(longitudinal="false", lateral="false"))

        # -----------------------------------------------------------------------------------
        #create an event for target
        #创建三个target事件
        trigcond = xosc.SimulationTimeCondition(0, xosc.Rule.greaterThan)
        trigger = xosc.ValueTrigger("target1_trigger_condition1",0,xosc.ConditionEdge.none,trigcond)
        event = xosc.Event("target1_event1", xosc.Priority.overwrite)
        event.add_trigger(trigger)

        sin_time = xosc.TransitionDynamics(xosc.DynamicsShapes.linear, xosc.DynamicsDimension.rate, 2.0)
        action = xosc.AbsoluteSpeedAction("$TargetSpeed", sin_time)
        event.add_action("target1_speed_action1", action)
        #事件2
        trigcond2=xosc.LanePosition(s="$Way_Trigger_Position",lane_id="$LaneId",road_id="$RoadId",offset=0)
        trigcond22=xosc.ReachPositionCondition(trigcond2,tolerance=1)
        trigger2=xosc.EntityTrigger("target1_trigger_condition2", 0, xosc.ConditionEdge.rising, trigcond22, egoname,triggeringpoint="start")
        event2=xosc.Event("target1_event2", xosc.Priority.overwrite)
        event2.add_trigger(trigger2)

        sin_time2 = xosc.TransitionDynamics(xosc.DynamicsShapes.linear, xosc.DynamicsDimension.rate,3.0)
        action2 = xosc.RelativeLaneChangeAction("$RelativeTargetLane_value",targetname,sin_time2)
        event2.add_action("target1_lanechange_action2", action2)
        #事件3
        trigcond3 = xosc.StoryboardElementStateCondition(element="action",reference="target1_lanechange_action2",state="endTransition")
        trigger3 = xosc.ValueTrigger("target1_trigger_condition3",0,xosc.ConditionEdge.none,trigcond3)
        event3 = xosc.Event("target1_event3", xosc.Priority.overwrite)
        event3.add_trigger(trigger3)

        sin_time3 = xosc.TransitionDynamics(xosc.DynamicsShapes.linear, xosc.DynamicsDimension.time, 3.9)
        action3 = xosc.AbsoluteSpeedAction("$TargetSpeed", sin_time3)
        event3.add_action("target1_speed_action3", action3)

        ## create the maneuver
        man = xosc.Maneuver("taget1_maneuver")
        man.add_event(event)
        man.add_event(event2)
        man.add_event(event3)
        mangr = xosc.ManeuverGroup("mangroup_target1")
        mangr.add_actor(targetname)
        mangr.add_maneuver(man)

        ### create two event for the ego
        #ego事件1
        ego_cond1 = xosc.StoryboardElementStateCondition(element="action",reference="target1_lanechange_action2",state="startTransition")
        ego_trigger1 = xosc.ValueTrigger("ego_trigger_condition1",0,xosc.ConditionEdge.none,ego_cond1,)
        ego_event1 = xosc.Event("ego_speedchange_event1", xosc.Priority.overwrite)
        ego_event1.add_trigger(ego_trigger1)

        ego_speed_change_action=xosc.SpeedProfileAction(["$EgoSpeed", "$RoadSpeedLimit","$EgoSetSpeed"], xosc.FollowingMode.position, [4, 5, 3])
        ego_event1.add_action("ego_start_action1", ego_speed_change_action)
        #ego事件2

        
        ## create the ego_maneuver
        ego_man = xosc.Maneuver("ego_maneuver")
        ego_man.add_event(ego_event1)
        #ego_man.add_event(ego_event2)

        ego_mangr = xosc.ManeuverGroup("mangroup_ego")
        ego_mangr.add_actor(egoname)
        ego_mangr.add_maneuver(ego_man)

        #故事板开始触发器
        sb_start_trigger_condition= xosc.SimulationTimeCondition(0, xosc.Rule.greaterThan)
        sb_start_trigger = xosc.ValueTrigger("Act_starttrigger",0,xosc.ConditionEdge.rising,sb_start_trigger_condition,"start")
        #动作集
        act = xosc.Act("my_act", sb_start_trigger)
        act.add_maneuver_group(mangr)
        act.add_maneuver_group(ego_mangr)

        ## create the storyboard
        sb_stop_trigger_condition = xosc.StoryboardElementStateCondition(element="action",reference="target1_lanechange_action2",state="endTransition")
        sb_stop_trigger=xosc.ValueTrigger("stop_simulation",21,xosc.ConditionEdge.rising,sb_stop_trigger_condition,"stop")
        sb = xosc.StoryBoard(init,sb_stop_trigger)
        sb.add_act(act)

        ## create the scenario
        sce = xosc.Scenario(
            "ACC_Straightline_follow",
            "lotus-team",
            paramdec,
            entities=entities,
            storyboard=sb,
            roadnetwork=road,
            catalog=catalog,
            osc_minor_version=self.open_scenario_version,
        )
        return sce


if __name__ == "__main__":
    mt = TableParse(path_excel)
    mt.parse()
    my_generalization=list(range(30,121,5))
    print(my_generalization)
    #print(mt.set_pd_names,mt.set_pd_values,mt.set_pd_types)
    #for i,j,n in zip(mt.set_pd_names,mt.set_pd_values,mt.set_pd_types):
        #print(i,"---",j,"---",n)

    for i,j in zip(my_generalization,range(len(my_generalization))):
        mt.set_pd_values[7]="${"+str(i)+"/3.6}"
        mt.set_pd_values[8]="${"+str(i)+"/3.6}"
        mt.set_pd_values[10]="${"+str(i)+"/3.6}"
        mt.set_pd_values[11]="${"+str(i+15)+"/3.6}"
        sce = Scenario().scenario(mt)
        my_xosc_filename= r"C:\Users\99062\Desktop\sim_xosc\sim_test\test_xosc\test"+str(j)+".xosc"
        sce.write_xml(filename=my_xosc_filename, prettyprint=True, encoding="utf-8")   
    #sce = Scenario().scenario(mt)
    # Print the resulting xml
    # prettyprint(sce.get_element())
    # write the OpenSCENARIO file as xosc using current script name
    #sce.write_xml(filename=r"C:\Users\99062\Desktop\sim_xosc\sim_test\test_xosc\test.xosc", prettyprint=True, encoding="utf-8")

    # uncomment the following lines to display the scenario using esmini
    # from scenariogeneration import esmini
    # esmini(sce,os.path.join('esmini'))
