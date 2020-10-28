import math

def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    closest_objects = params['closest_objects']
    closest_waypoints = params['closest_waypoints']
    distance_from_center = params['distance_from_center']
    heading = params['heading']
    objects_distance = params['objects_distance']
    progress = params['progress']
    waypoints = params['waypoints']
    speed = params['speed']
    track_width = params['track_width']
    track_length = params['track_length']

    half_track_width = track_width / 2
​
    DIRECTION_THRESHOLD = 10.0
    MIN_DISTANCE = 0.5

    reward = 0.001
​
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
​
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)
​
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    back_car = closest_objects[0]
    front_car = closest_objects[1]
    distance_from_front_car = abs(objects_distance[front_car] - (progress / 100.0) * track_length)

    faster = (speed ** 2)
    closer_to_center = ((1 - (distance_from_center / half_track_width)) * 2) ** 2
    steering_correctly = ((1 - (direction_diff / DIRECTION_THRESHOLD)) * 2) ** 2
    farther_from_front_car = (distance_from_front_car / MIN_DISTANCE)

    if all_wheels_on_track and direction_diff < DIRECTION_THRESHOLD:
        reward += faster + closer_to_center
        reward += steering_correctly
    else:
        reward -= (speed ** 2) + (distance_from_center ** 2) + (direction_diff ** 2)

    if not (distance_from_front_car < MIN_DISTANCE and (objects_left_of_center[front_car] == is_left_of_center)):
        reward += farther_from_front_car
    else:
        reward -= distance_from_front_car

    return float(reward)
