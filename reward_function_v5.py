import math

def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    closest_objects = params['closest_objects']
    closest_waypoints = params['closest_waypoints']
    distance_from_center = params['distance_from_center']
    heading = params['heading']
    is_left_of_center = params['is_left_of_center']
    objects_distance = params['objects_distance']
    objects_left_of_center = params['objects_left_of_center']
    progress = params['progress']
    waypoints = params['waypoints']
    speed = params['speed']
    steps = params['steps']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    track_length = params['track_length']
    abs_steering_angle = abs(steering_angle)

    half_track_width = track_width / 2

    DIRECTION_THRESHOLD = 10.0
    MIN_DISTANCE = 1.5

    reward = 0.001

    front_car = closest_objects[1]
    distance_from_front_car = abs(objects_distance[front_car] - (progress / 100.0) * track_length)

    faster = round(speed ** 2, 3)

    if all_wheels_on_track:
        if steps > 10:
            reward += progress / steps

    if abs_steering_angle < 10 and speed > 2:
        reward += faster
    else:
        reward += 0.01

    if distance_from_front_car <= MIN_DISTANCE:
        ideal_track = half_track_width - 0.2
        if objects_left_of_center[front_car]: # car in front on left lane
            if not is_left_of_center and abs(distance_from_center - ideal_track) < 0.2: # if my car is on right lane
                reward += faster
            if is_left_of_center: # if my car is on left lane
                reward += 0.01
        else: # car in front on right lane
            if is_left_of_center and abs(distance_from_center - ideal_track) < 0.2: # if my car is on left lane
                reward += faster
            if not is_left_of_center:
                reward += 0.01

    return float(reward)
