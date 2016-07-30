from Robot import Ferriclean
import threading

ctw_robot = Ferriclean()
t1 = threading.Thread(name = 'Obstacle Avoidance', target = ctw_robot.obstacle_avoidance)
t2 = threading.Thread(name = 'Brush Control', target = ctw_robot.brushcontrol)
t1.start()
t2.start()
