function updateBedStatus() {
  fetch("/api/bed-status")
    .then((response) => response.json())
    .then((beds) => {
      const container = document.getElementById("bed-container");
      container.innerHTML = "";

      beds.forEach((bed) => {
        const bedDiv = document.createElement("div");
        bedDiv.className = "col-md-4";
        bedDiv.innerHTML = `
                    <div class="bed-card ${
                      bed.occupied ? "occupied" : "vacant"
                    }">
                        <h3>床位 ${bed.bed_number}</h3>
                        <p>温度: ${bed.temperature}°C</p>
                        <p>湿度: ${bed.humidity}%</p>
                        <p>状态: ${bed.occupied ? "已占用" : "空闲"}</p>
                        ${
                          bed.occupied
                            ? `
                            <p>患者: ${bed.patient_name}</p>
                            <button class="btn btn-primary btn-sm" 
                                onclick="showChatHistory(${bed.patient_id})">
                                查看聊天记录
                            </button>
                        `
                            : ""
                        }
                    </div>
                `;
        container.appendChild(bedDiv);
      });
    });
}

function showChatHistory(patientId) {
  fetch(`/api/chat-history/${patientId}`)
    .then((response) => response.json())
    .then((chats) => {
      const chatHistory = document.getElementById("chat-history");
      chatHistory.innerHTML = "";

      chats.forEach((chat) => {
        const messageDiv = document.createElement("div");
        messageDiv.className = `chat-message ${
          chat.is_patient ? "patient-message" : "ai-message"
        }`;
        messageDiv.innerHTML = `
                    <small class="text-muted">${chat.timestamp}</small>
                    <p class="mb-0">${chat.message}</p>
                `;
        chatHistory.appendChild(messageDiv);
      });

      $("#chatModal").modal("show");
    });
}

// 每30秒更新一次床位状态
updateBedStatus();
setInterval(updateBedStatus, 30000);
