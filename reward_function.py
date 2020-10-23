import math

def reward_function(params):

    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    closest_objects = params['closest_objects']
    objects_distance = params['objects_distance']
    progress = params["progress"]
    track_length = params["track_length"]
    objects_left_of_center = params['objects_left_of_center']
    is_left_of_center = params['is_left_of_center']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering_angle = params['steering_angle']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    reward = 0

    def all_wheels_on_track_and_fast(all_wheels_on_track, speed):
        SPEED_THRESHOLD = 1
        # Penalize if the car goes off track
        if not all_wheels_on_track:
            reward = 1e-3
            # Penalize if the car goes too slow
        elif speed < SPEED_THRESHOLD:
            reward = 0.5
            # High reward if the car stays on track and goes fast
        else:
            reward = 1.0
        return float(reward)

    def do_not_get_too_close(closest_objects, objects_distance, progress, track_length, objects_left_of_center, is_left_of_center):
        MIN_DISTANCE = 0.5

        back_car = closest_objects[0]
        front_car = closest_objects[1]
        distance_from_front_car = abs(objects_distance[front_car] - (progress/100.0)*track_length)

        ## our car is too close to the front car and our car is on the same lane as the other car
        if distance_from_front_car < MIN_DISTANCE and (objects_left_of_center[front_car] == is_left_of_center):
            reward = 1e-3
        else:
            reward = 1.0
        return float(reward)

    def avoid_steering(track_width, distance_from_center, steering_angle):
	    # Calculate 3 marks that are farther and father away from the center line
    	marker_1 = 0.1 * track_width
    	marker_2 = 0.25 * track_width
    	marker_3 = 0.5 * track_width

    	# Give higher reward if the car is closer to center line and vice versa
    	if distance_from_center <= marker_1:
    		reward = 1
    	elif distance_from_center <= marker_2:
    		reward = 0.5
    	elif distance_from_center <= marker_3:
    		reward = 0.1
    	else:
    		reward = 1e-3  # likely crashed/ close to off track

    	# # Steering penality threshold, change the number based on your action space setting
    	# ABS_STEERING_THRESHOLD = 15
        #
    	# # Penalize reward if the car is steering too much
    	# if abs(steering_angle) > ABS_STEERING_THRESHOLD:  # Only need the absolute steering angle
    	# 	reward *= 0.5
        return float(reward)

    def turn_when_road_is_turning(waypoints, closest_waypoints, heading):
        # Initialize the reward with typical value
        reward = 1.0

        # Calculate the direction of the center line based on the closest waypoints
        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]

        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
        # Convert to degree
        track_direction = math.degrees(track_direction)

        # Calculate the difference between the track direction and the heading direction of the car
        direction_diff = abs(track_direction - heading)
        if direction_diff > 180:
            direction_diff = 360 - direction_diff

        # Penalize the reward if the difference is too large
        DIRECTION_THRESHOLD = 10.0
        if direction_diff > DIRECTION_THRESHOLD:
            reward = 1e-3

    	return float(reward)

    def add_weight(weight, reward_func):
        return reward_func * weight;

    reward += add_weight(2, all_wheels_on_track_and_fast(all_wheels_on_track, speed))
    reward += add_weight(1, do_not_get_too_close(closest_objects, objects_distance, progress, track_length, objects_left_of_center, is_left_of_center))
    reward += add_weight(1.5, avoid_steering(track_width, distance_from_center, steering_angle))
    reward += add_weight(1.5, turn_when_road_is_turning(waypoints, closest_waypoints, heading))

    return reward
