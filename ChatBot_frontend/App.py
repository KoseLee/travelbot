import streamlit as st
import requests

# Định nghĩa địa chỉ API của FastAPI
API_URL = "http://127.0.0.1:8001"

# Tiêu đề của ứng dụng
st.title('Travel Bot')

# Khung nhập dữ liệu từ người dùng
user_input = st.text_area('Nhập câu hỏi của bạn về du lịch:', '')

# Sử dụng session_state để lưu trữ lịch sử cuộc trò chuyện
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Nút gửi để gửi yêu cầu đến API
if st.button('Gửi'):
    if user_input.strip():
        # Gửi yêu cầu POST đến API FastAPI
        try:
            response = requests.post(f"{API_URL}/travel-rag", json={"text": user_input})
            if response.status_code == 200:
                try:
                    data = response.text  # Lấy dữ liệu như là một chuỗi
                    # Thêm tin nhắn vào lịch sử cuộc trò chuyện
                    st.session_state.chat_history.append({"question": user_input, "answer": data})
                    
                    # Hiển thị lịch sử cuộc trò chuyện trên giao diện
                    st.write("### Lịch sử cuộc trò chuyện")
                    for message in st.session_state.chat_history[-5:]:  # Chỉ hiển thị 5 tin nhắn gần nhất
                        st.write(f"**You:** {message['question']}")
                        st.write(f"**Bot:** {message['answer']}")
                except ValueError:
                    st.error("Dữ liệu trả về từ API không hợp lệ")
            else:
                st.error(f"Lỗi khi gửi yêu cầu: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Lỗi kết nối đến API: {str(e)}")
    else:
        st.warning("Vui lòng nhập câu hỏi trước khi gửi!")

# Hiển thị các câu hỏi và câu trả lời đã hỏi
st.write("### Lịch sử câu hỏi và trả lời")
if st.session_state.chat_history:
    for message in st.session_state.chat_history[-5:]:  # Chỉ hiển thị 5 tin nhắn gần nhất
        st.write(f"**You:** {message['question']}")
        st.write(f"**Bot:** {message['answer']}")
else:
    st.write("Chưa có câu hỏi nào được hỏi.")

# Thêm phần thống kê câu hỏi đã hỏi
st.write("### Thống kê câu hỏi đã hỏi")
if st.session_state.chat_history:
    question_count = len(st.session_state.chat_history)
    st.write(f"Tổng số câu hỏi đã hỏi: {question_count}")
else:
    st.write("Chưa có câu hỏi nào được hỏi.")
