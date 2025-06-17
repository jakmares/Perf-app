def update_icon(hostname, is_alive, status_labels, ok_img, nok_img):
    label = status_labels.get(hostname)
    if label:
        new_icon = ok_img if is_alive else nok_img
        label.config(image=new_icon)
        label.image = new_icon

def update_jmeter_icon(hostname, is_alive, server_status, ok_img, nok_img):
    label = server_status.get(hostname)
    if label:
        new_icon = ok_img if is_alive else nok_img
        label.config(image=new_icon)
        label.image = new_icon

def schedule_ping(root, refresh_time, ping_func, update_callback):
    ping_func(update_callback)
    root.after(refresh_time, lambda: schedule_ping(root, refresh_time, ping_func, update_callback))

def schedule_jmeter_check(root, refresh_time, jmeter_func, update_callback):
    jmeter_func(update_callback)
    root.after(refresh_time, lambda: schedule_jmeter_check(root, refresh_time, jmeter_func, update_callback))
