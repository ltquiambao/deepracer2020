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
    track_width = params['track_width']
    track_length = params['track_length']

    half_track_width = track_width / 2

    DIRECTION_THRESHOLD = 10.0
    MIN_DISTANCE = 1.5

    reward = 0.001

    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)

    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # back_car = closest_objects[0]
    front_car = closest_objects[1]
    distance_from_front_car = abs(objects_distance[front_car] - (progress / 100.0) * track_length)
    # distance_from_back_car = abs(objects_distance[back_car] - (progress / 100.0) * track_length)

    faster = round(speed ** 2, 3)
    closer_to_center = round(((1 - (distance_from_center / half_track_width)) * 2) ** 3, 3)
    # steering_correctly = round(((1 - (direction_diff / DIRECTION_THRESHOLD)) * 2) ** 2, 3)

    if all_wheels_on_track and (direction_diff < DIRECTION_THRESHOLD):
        x = max(faster + closer_to_center, 0.01)
        if steps < 10:
            reward = x # max reward 8
        elif steps >= 10:
            reward = (progress * x / steps) * 2
    else:
        reward = 0.01

    if distance_from_front_car <= MIN_DISTANCE:
        ideal_track = half_track_width - 0.1
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
