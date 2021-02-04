# address = 'b2blk.megafon.ru'
SIZE = 40 
# sim_count = 735
# url = 'https://{address}/ws/v1.0/subscriber/mobile/list?from={start}&size={size}'
    
def calc_requests(sim_count: int, SIZE: int) -> dict:
    
    start = [0,]
    count_requests = sim_count // SIZE
    if count_requests > 0:
        for i in range(1, count_requests+1):
            start.append(SIZE*i)
    requests_dict = {'count': count_requests, 'start': start}
    last_step = sim_count - start[-1] if len(start) > 1 else sim_count - SIZE
    if last_step > 0:
        requests_dict['last_step'] = last_step
    if last_step < 0:
        requests_dict['last_step'] = SIZE + last_step
    
    return requests_dict


def get_urls_simList(sim_count: int, url: str, SIZE: int, address: str):

    calc = calc_requests(sim_count, SIZE)
    urls_list = []
    size = SIZE
    if calc['count'] == 0 and 'last_step' in calc:
        size = calc['last_step']
        request_url = url.format(address=address, start=0, size=size)
        urls_list.append(request_url)
    elif calc['count'] >= 1:
        for start in calc['start']:
            if start == calc['start'][-1] and 'last_step' in calc:
                size = calc['last_step']
            if start == calc['start'][-1] and 'last_step' not in calc:
                break
            request_url = url.format(address=address, start=start, size=size)
            urls_list.append(request_url)
    return urls_list

# print(get_urls_simList(sim_count, url, SIZE, address))