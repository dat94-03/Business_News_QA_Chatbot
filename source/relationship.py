import os, json
import random
# file_path = next((os.path.join(root, 'input.json') for root, dirs, files in os.walk('/path/to/start/search') if name in files), 'File not found')
event_path = '/Users/nguyenbathiem/Documents/GitHub/Business_News_QA_Chatbot-1/source/events.json'
with open(event_path) as f:
    events = json.load(f)
    
similarity_path = '/Users/nguyenbathiem/Documents/GitHub/Business_News_QA_Chatbot-1/source/output.json'
with open(similarity_path) as f:
    similarities = json.load(f)

import time
import json
import traceback
import openai
from tqdm import tqdm
from  apikey import api_keys

# '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'
# nguyenbathiemoutlookcom, 'yctl', hacaominthu, hoangdungforwork
current_key_index = 0
start = time.time()

openai.api_key = api_keys[current_key_index]
threshold = 0.6 
# threshold = 0.7
# threshold = 0.8
stop_index = 0
def AI(prompt:str,engine ="gpt-3.5-turbo"):
    completion = openai.ChatCompletion.create(
    model = engine,
    messages = [{'role': 'user', 'content': prompt}],
    max_tokens= 100,
    temperature = 0.2)
    response=completion['choices'][0]['message']['content']
    return response
# Assuming similarities, events, and AI are already defined
pbar = tqdm(total=len(similarities[stop_index:]), desc="Processing Pairs")
for i ,similarity in enumerate(similarities):
    if i < stop_index:
        continue
    id1 = str(similarity['id1'])
    id2 = str(similarity['id2'])
    cos = similarity['cost']
    event1 = events[id1]
    event2 = events[id2]
    prompt = f'''Classify the event relationship between two below news into 2 type of event relationships: CASUAL or COREFERENCE relationship. Know that: 
- A causal relationship means that one event caused the other event to happen; 
- On the other hand, coreference event relationships refer to the grouping of event mentions referring to the same real-world event into clusters.
Do not explain anything, just return one of two relationships above.
###Example###
Exmaple 1:
Event 1: Ngân hàng TMCP Công Thương Việt Nam (VietinBank) vừa công bố biểu lãi suất huy động mới với việc điều chỉnh giảm 0,2 – 0,3 điểm % tại các kỳ hạn từ 3 tháng trở lên. Cụ thể, lãi suất tiền gửi không kỳ hạn và các kỳ hạn dưới 1 tháng được giữ nguyên ở mức 0,1% và 0,2%; các kỳ hạn từ 1 tháng đến dưới 3 tháng vẫn được hưởng lãi suất 3%/năm. Trong khi đó, lãi suất các kỳ hạn từ 3 tháng đến dưới 6 tháng giảm từ 3,8% xuống 3,5%/năm; kỳ hạn từ 6 tháng đến dưới 12 tháng giảm từ 4,7% xuống 4,5%/năm. Các kỳ hạn từ 12 tháng trở lên đang được VietinBank áp dụng mức lãi suất huy động cao nhất là 5,5%/năm, giảm 0,3 điểm % so với trước đó.
Event 2: Trước đó, Vietcombank và Agribank cũng đã giảm 0,2-0,3 điểm % lãi suất tiền gửi từ ngày 14/9, đưa lãi suất cao nhất xuống còn 5,5%/năm. Đến ngày 18/9, BIDV cũng có động thái tương tự khi giảm 0,2-0,3 điểm % ở hàng loạt kỳ hạn. Như vậy, toàn bộ nhóm 4 ngân hàng quốc doanh là VietinBank, Vietcombank, BIDV và Agribank đều đã giảm lãi suất huy động cao nhất xuống còn 5,5%/năm - ngang mức thấp lịch sử ghi nhận trong giai đoạn covid-19. Hiện lãi suất của 4 ngân hàng này khá tương đương nhau, chỉ có một số khác biệt ở hình thức tiết kiệm online nhưng không đáng kể.
Result: Coreference

Exmaple 2:
Event 1: Khi Ngân hàng Nhà nước ưu tiên hạ lãi suất cho vay, điều này sẽ dẫn đến giảm lượng tiền cung ứng trong nền kinh tế.
Event 2: Khi lượng tiền cung ứng giảm, nhu cầu ngoại tệ để thanh toán cho các hoạt động nhập khẩu, thanh toán nợ nước ngoài và đầu tư nước ngoài sẽ tăng lên. Điều này sẽ tạo áp lực lên tỷ giá và khiến đồng VND yếu đi.
Result: Casual

###Data###
Event 1: {event1}
Event 2: {event2}
Result:
''' 
    
    while True:  # Add a loop to retry after handling exceptions
        try:
            dir_path = '/Users/nguyenbathiem/Documents/GitHub/Business_News_QA_Chatbot-1/source/'
            with open(dir_path + 'relationship.json', 'r') as f:
                results_json = json.load(f)
            
            if str(threshold) not in results_json:
                results_json[str(threshold)] = []
            dic = results_json[str(threshold)]
            
            con = 0
            for result in dic:
                if result['id1'] == id1 and result['id2'] == id2:
                    con = 1
                    break
                elif result['id1'] == id2 and result['id2'] == id1:
                    con = 1
                    break
            if con == 1:
                pbar.update(1)
                break
            if cos >= threshold:
                results = {'id1': id1, 'id2': id2, 'relationship':AI(prompt)}
                time.sleep(random.randint(2, 5))
            else:
                results = {'id1': id1, 'id2': id2, 'relationship': None}
                
            dic.append(results)
            with open(dir_path + 'relationship.json', 'w') as f:
                json.dump(results_json, f, ensure_ascii=False, indent=4)
            pbar.update(1)  # Update the progress bar
            break  # If everything goes well, break out of the loop

        except Exception as e:
            if 'Rate limit reached' in str(e):
                # Rotate to the next API key
                current_key_index = (current_key_index + 1) % len(api_keys)
                openai.api_key = api_keys[current_key_index]
                
                # If we've looped through all keys, wait
                if current_key_index == 0:
                    # Calculate the sleep time as needed
                    end = time.time()
                    time.sleep(max(60 - (end - start), 1))  # Ensure at least 1 second sleep
                    start = time.time()
                # Optionally log which key is now active
                print(f'index: {i}, error id1: {id1}, error id2: {id2}')
                print(f"Switched to API key index: {current_key_index}. Retrying...")
            
            elif 'You exceeded your current quota' in str(e) or 'Incorrect API key provided'in str(e):
                print("You exceeded your current quota, please check your plan and billing details.")
                print(f'index: {i}, error id1: {id1}, error id2: {id2}')
                api_keys.remove(api_keys[current_key_index])
                if len(api_keys) == 0:
                    print('No more API key')
                    break
                
            else:
                print(f'index: {i}, error id1: {id1}, error id2: {id2}')
                traceback.print_exc()  # Print the stack trace to understand the exception
                break

pbar.close()