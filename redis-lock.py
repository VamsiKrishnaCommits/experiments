import threading
import redis
import time

def increment_counter(redis_client, lock, thread_id):
    with lock:
        # Critical section: only one thread can execute this at a time
        current_value = int(redis_client.get('counter') or 0)
        print(f"Thread {thread_id}: Current Counter Value = {current_value}")
        new_value = current_value + 1
        time.sleep(1)  # Simulate some processing time
        redis_client.set('counter', new_value)
        print(f"Thread {thread_id}: New Counter Value = {new_value}")

def main():
    client = redis.Redis(host='localhost', port=6379, db=0)
    client.set('counter', 0)  # Initialize the counter
    
    lock = client.lock('counter_lock', timeout=5)

    threads = []

    for i in range(5):
        thread = threading.Thread(target=increment_counter, args=(client, lock, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Final Counter Value:", client.get('counter').decode('utf-8'))

if __name__ == "__main__":
    main()
