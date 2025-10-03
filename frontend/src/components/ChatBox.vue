<template>
  <div class="chat-container">
    <div class="chat-header">
      <h2>📚 Story Assistant</h2>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div 
        v-for="(msg, index) in messages" 
        :key="index"
        :class="['message', msg.role]"
      >
        <div class="message-content">
          <p>{{ msg.content }}</p>
          <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
        </div>
      </div>

      <div v-if="isLoading" class="message assistant">
        <div class="message-content">
          <p>Typing...</p>
        </div>
      </div>
    </div>

    <div v-if="generatedStory" class="story-display">
      <h3>✨ Your Story</h3>
      <div class="story-content">{{ generatedStory }}</div>
      <button @click="startNewStory" class="new-story-btn">
        New Story
      </button>
    </div>

    <div class="chat-input">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="Type your message..."
        :disabled="isLoading"
      />
      <button @click="sendMessage" :disabled="isLoading || !userInput.trim()">
        Send
      </button>
    </div>
  </div>
</template>

<script>
import { ref, nextTick } from 'vue';
import { chatAPI } from '../services/api';

export default {
  name: 'ChatBox',
  setup() {
    const messages = ref([]);
    const userInput = ref('');
    const isLoading = ref(false);
    const sessionId = ref(null);
    const generatedStory = ref(null);
    const messagesContainer = ref(null);

    const formatTime = (timestamp) => {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    };

    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
        }
      });
    };

    const sendMessage = async () => {
      if (!userInput.value.trim() || isLoading.value) return;

      const message = userInput.value.trim();
      
      messages.value.push({
        role: 'user',
        content: message,
        timestamp: new Date()
      });

      userInput.value = '';
      isLoading.value = true;
      scrollToBottom();

      try {
        const response = await chatAPI.sendMessage(message, sessionId.value);
        
        sessionId.value = response.session_id;

        messages.value.push({
          role: 'assistant',
          content: response.message,
          timestamp: new Date()
        });

        if (response.story) {
          generatedStory.value = response.story;
        }

        scrollToBottom();
      } catch (error) {
        messages.value.push({
          role: 'assistant',
          content: 'Sorry, an error occurred. Please try again.',
          timestamp: new Date()
        });
      } finally {
        isLoading.value = false;
      }
    };

    const startNewStory = () => {
      messages.value = [];
      sessionId.value = null;
      generatedStory.value = null;
      userInput.value = 'new story';
      sendMessage();
    };

    const init = async () => {
      userInput.value = 'Hello';
      await sendMessage();
    };

    init();

    return {
      messages,
      userInput,
      isLoading,
      generatedStory,
      messagesContainer,
      sendMessage,
      startNewStory,
      formatTime
    };
  }
};
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.chat-header {
  background: #4CAF50;
  color: white;
  padding: 20px;
  text-align: center;
}

.chat-header h2 {
  margin: 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: white;
}

.message {
  margin-bottom: 15px;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  position: relative;
}

.user .message-content {
  background: #4CAF50;
  color: white;
}

.assistant .message-content {
  background: #e0e0e0;
  color: #333;
}

.message-content p {
  margin: 0 0 5px 0;
  white-space: pre-wrap;
}

.timestamp {
  font-size: 11px;
  opacity: 0.7;
}

.story-display {
  background: #fff3cd;
  padding: 20px;
  margin: 20px;
  border-radius: 12px;
  border: 2px solid #ffc107;
}

.story-display h3 {
  margin-top: 0;
  color: #856404;
}

.story-content {
  white-space: pre-wrap;
  line-height: 1.6;
  margin: 15px 0;
}

.new-story-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.new-story-btn:hover {
  background: #45a049;
}

.chat-input {
  display: flex;
  padding: 20px;
  background: white;
  border-top: 1px solid #ddd;
}

.chat-input input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 24px;
  font-size: 14px;
  outline: none;
}

.chat-input input:focus {
  border-color: #4CAF50;
}

.chat-input button {
  margin-left: 10px;
  padding: 12px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  font-size: 14px;
}

.chat-input button:hover:not(:disabled) {
  background: #45a049;
}

.chat-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>