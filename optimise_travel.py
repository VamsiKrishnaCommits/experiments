import streamlit as st
import googlemaps
from datetime import datetime
import os

# Your Python function here (optimize_child_travel_time)
def optimize_child_travel_time(pickup_points, destination, num_cars, capacity_per_car):
    gmaps = googlemaps.Client(key=os.environ['API_KEY'])
    # Initialize routes list for each car with detailed information
    routes = [{'pickups': [], 'total_in_car_time': 0, 'route_info': []} for _ in range(num_cars)]

    # Ensure destination is in coordinate form (latitude, longitude)
    destination_coords = (destination['lat'], destination['lng'])

    while pickup_points:
        best_assignment = (None, None, float('inf'))

        for car_index, car in enumerate(routes):
            if len(car['pickups']) >= capacity_per_car:
                continue

            current_location =  destination_coords
            for pickup_index, pickup in enumerate(pickup_points):
                pickup_coords = (pickup['location']['lat'], pickup['location']['lng'])
                # Calculate the impact of adding this pickup to the route
                proposed_route = car['pickups'] + [pickup]
                total_route_time = 0
                last_location = current_location

                for stop in proposed_route:
                    stop_coords = (stop['location']['lat'], stop['location']['lng'])
                    # Calculate from the last location to the next stop
                    leg = gmaps.distance_matrix(stop_coords, last_location, mode="driving")['rows'][0]['elements'][0]
                    total_route_time += leg['duration']['value']
                    last_location = stop_coords

                if total_route_time < best_assignment[2]:
                    best_assignment = (car_index, pickup_index, total_route_time)

        # Assign the best pickup to the appropriate car
        if best_assignment[0] is not None:
            car_index, pickup_index = best_assignment[0], best_assignment[1]
            car = routes[car_index]
            pickup = pickup_points.pop(pickup_index)
            car['pickups'].append(pickup)
            car['total_in_car_time'] = best_assignment[2]
            # Add detailed route info including labels and coordinates
            car['route_info'].append({
                'label': pickup.get('label', 'No Label'),
                'time_spent_by_child_in_minutes': int(best_assignment[2]/60),
                'location': pickup['location']
            })

    return routes
     


def main():
    st.title("Travel time optimiser")

    # User specifies the number of pickup points
    num_pickups = st.number_input("Enter number of pickup points:", min_value=0, value=0, step=1)
    pickup_points = []

    # Dynamic input fields for each pickup point
    for i in range(num_pickups):
        coords_input = st.text_input(f"Enter lat, long for Pickup {i+1} (format: lat,long):", key=f"pickup_{i}")
        if coords_input:
            lat, lng = map(float, coords_input.split(','))
            pickup_points.append({'location': {'lat': lat, 'lng': lng}, 'label': f"Pickup {i+1}"})

    # User input for destination
    dest_coords_input = st.text_input("Enter destination lat, long (format: lat,long):", "0.0,0.0")
    if dest_coords_input:
        dest_lat, dest_lng = map(float, dest_coords_input.split(','))
        destination = {'lat': dest_lat, 'lng': dest_lng}

    # Selection sliders for cars and capacity
    num_cars = st.slider("Select Number of Cars", 1, 100, 2)
    capacity_per_car = st.slider("Select Capacity per Car", 1, 100, 3)

    # Button to optimize route
    if st.button("Optimize Route") and destination and pickup_points:
        routes = optimize_child_travel_time(pickup_points, destination, num_cars, capacity_per_car)
        st.write("Generated Routes:")
        for i, route in enumerate(routes):
            st.write(f"Car {i+1}:")
            route.get('route_info').reverse()  # Assuming this is meant to display the route in reverse order
            st.write(route.get('route_info'))

if __name__ == "__main__":
    main()
