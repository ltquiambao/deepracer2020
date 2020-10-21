def reward_function(params):
    ### more reward farther from other bots
    ### if there's something in front of me go on the other lane, speed up
    ### reward if on center of track
    ### reward if there's nothing in front of me

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

    reward = 0

    def all_wheels_on_track_and_fast(all_wheels_on_track, speed):
      SPEED_THRESHOLD = 1.0
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
            reward = 0.5
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

    	# Steering penality threshold, change the number based on your action space setting
    	ABS_STEERING_THRESHOLD = 15

    	# Penalize reward if the car is steering too much
    	if abs(steering_angle) > ABS_STEERING_THRESHOLD:  # Only need the absolute steering angle
    		reward *= 0.5

    	return float(reward)

    reward += all_wheels_on_track_and_fast(all_wheels_on_track, speed)
    reward += do_not_get_too_close(closest_objects, objects_distance, progress, track_length, objects_left_of_center, is_left_of_center)
    reward += avoid_steering(track_width, distance_from_center, steering_angle)

    return reward
