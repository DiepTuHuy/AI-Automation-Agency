document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const volumesList = document.getElementById('volumes-list');
  const markdownSection = document.getElementById('markdown-section');
  const activePath = document.getElementById('active-path');
  const openConfigBtn = document.getElementById('open-config-btn');
  const closeConfigBtn = document.getElementById('close-config-btn');
  const saveConfigBtn = document.getElementById('save-config-btn');
  const configModal = document.getElementById('config-modal');
  const apiKeyInput = document.getElementById('api-key-input');
  const quizArea = document.getElementById('quiz-area');
  const searchInput = document.getElementById('search-input');
  const progressBarFill = document.getElementById('progress-bar-fill');
  const progressPercentage = document.getElementById('progress-percentage');
  const completeBtnContainer = document.getElementById('complete-btn-container');
  const markCompleteBtn = document.getElementById('mark-complete-btn');
  
  // Drawer Elements
  const openQuizBtn = document.getElementById('open-quiz-btn');
  const closeQuizBtn = document.getElementById('close-quiz-btn');
  const drawerBackdrop = document.getElementById('drawer-backdrop');

  let currentVolume = '';
  let currentChapter = '';
  let currentFilePath = '';
  let allChaptersList = []; // Track all files to calculate progress
  let lastSelectedDifficulty = 'medium';
  let lastSelectedLimit = 5;

  // Configure marked parser options
  marked.setOptions({
    breaks: true,
    gfm: true
  });

  // Modal actions
  openConfigBtn.addEventListener('click', () => {
    configModal.style.display = 'flex';
    const key = localStorage.getItem('gemini_api_key');
    if (key) {
      apiKeyInput.placeholder = '••••••••••••••••••••••••';
    } else {
      apiKeyInput.placeholder = 'AIzaSy...';
    }
  });

  closeConfigBtn.addEventListener('click', () => {
    configModal.style.display = 'none';
  });

  saveConfigBtn.addEventListener('click', () => {
    const key = apiKeyInput.value.trim();
    if (!key) {
      alert('Vui lòng nhập API Key hợp lệ!');
      return;
    }
    localStorage.setItem('gemini_api_key', key);
    alert('Đã lưu cấu hình API Key vào trình duyệt!');
    configModal.style.display = 'none';
    apiKeyInput.value = '';
  });

  // Quiz Drawer Toggling
  openQuizBtn.addEventListener('click', () => {
    document.body.classList.add('quiz-open');
  });

  function closeQuizDrawer() {
    document.body.classList.remove('quiz-open');
    document.body.classList.remove('sidebar-open');
  }

  closeQuizBtn.addEventListener('click', closeQuizDrawer);
  drawerBackdrop.addEventListener('click', closeQuizDrawer);

  // Mobile Sidebar Toggle button
  const sidebarToggleBtn = document.getElementById('sidebar-toggle-btn');
  if (sidebarToggleBtn) {
    sidebarToggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('sidebar-open');
    });
  }

  // Close drawer on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeQuizDrawer();
      configModal.style.display = 'none';
    }
  });

  // Search filter functionality
  searchInput.addEventListener('input', (e) => {
    const keyword = e.target.value.toLowerCase().trim();
    const volumeGroups = document.querySelectorAll('.volume-group');
    
    volumeGroups.forEach(group => {
      const headerText = group.querySelector('.volume-header').textContent.toLowerCase();
      const chapters = group.querySelectorAll('.chapter-item');
      let matchesAnyChapter = false;

      chapters.forEach(chap => {
        const chapText = chap.textContent.toLowerCase();
        if (chapText.includes(keyword)) {
          chap.style.display = 'flex';
          matchesAnyChapter = true;
        } else {
          chap.style.display = 'none';
        }
      });

      if (headerText.includes(keyword) || matchesAnyChapter) {
        group.style.display = 'block';
        if (keyword !== '') {
          group.classList.add('active'); // Expand matching volumes
        } else {
          group.classList.remove('active');
        }
      } else {
        group.style.display = 'none';
      }
    });
  });

  // Load completed progress from LocalStorage
  function getCompletedChapters() {
    const data = localStorage.getItem('completed_chapters');
    return data ? JSON.parse(data) : [];
  }

  function markChapterComplete(path) {
    const completed = getCompletedChapters();
    if (!completed.includes(path)) {
      completed.push(path);
      localStorage.setItem('completed_chapters', JSON.stringify(completed));
    }
    updateProgressUI();
    renderCompletedIcons();
  }

  // Calculate and update progress bar
  function updateProgressUI() {
    if (allChaptersList.length === 0) return;
    const completed = getCompletedChapters();
    const completedCount = completed.filter(path => allChaptersList.includes(path)).length;
    const percent = Math.round((completedCount / allChaptersList.length) * 100);
    
    progressBarFill.style.width = `${percent}%`;
    progressPercentage.textContent = `Tiến độ: ${percent}%`;
  }

  // Highlight checkmark icons in sidebar
  function renderCompletedIcons() {
    const completed = getCompletedChapters();
    document.querySelectorAll('.chapter-item').forEach(el => {
      const path = el.getAttribute('data-path');
      if (completed.includes(path)) {
        el.classList.add('completed-chapter');
      } else {
        el.classList.remove('completed-chapter');
      }
    });
  }

  // Setup Complete Button event
  markCompleteBtn.addEventListener('click', () => {
    if (markCompleteBtn.classList.contains('completed')) return;
    
    markChapterComplete(currentFilePath);
    
    markCompleteBtn.textContent = '✓ Đã hoàn thành chương';
    markCompleteBtn.classList.add('completed');
  });

  // Load sidebar data (fetch volumes.json from the repository root)
  function loadSidebar() {
    fetch('./volumes.json')
      .then(res => {
        if (!res.ok) throw new Error('Không thể đọc file volumes.json');
        return res.json();
      })
      .then(volumes => {
        volumesList.innerHTML = '';
        allChaptersList = [];
        
        const projectsVol = volumes.find(v => v.name === 'Projects');
        const courseVolumes = volumes.filter(v => v.name !== 'Projects').sort((a, b) => a.name.localeCompare(b.name));
        
        const allVols = [...courseVolumes];
        if (projectsVol) {
          allVols.push(projectsVol);
        }

        allVols.forEach(vol => {
          const volEl = document.createElement('div');
          volEl.className = 'volume-group';
          
          const header = document.createElement('div');
          header.className = 'volume-header';
          const cleanVolName = vol.name.replace(/-/g, ' ');
          header.innerHTML = `<span>📂 ${cleanVolName}</span> <span>▼</span>`;
          
          const chaptersEl = document.createElement('div');
          chaptersEl.className = 'volume-chapters';
          
          vol.files.sort().forEach(file => {
            const chapEl = document.createElement('div');
            chapEl.className = 'chapter-item';
            
            const fileFullPath = vol.path + '/' + file;
            allChaptersList.push(fileFullPath); // Add to progress calculator
            chapEl.setAttribute('data-path', fileFullPath);

            const cleanFileName = file.replace(/^\d+-/, '').replace(/-/g, ' ').replace('.md', '');
            chapEl.textContent = cleanFileName === 'README' ? '★ Giới thiệu Volume' : `• ${cleanFileName}`;
            
            chapEl.addEventListener('click', (e) => {
              e.stopPropagation();
              document.querySelectorAll('.chapter-item').forEach(item => item.classList.remove('active'));
              chapEl.classList.add('active');
              
              loadChapter(vol.name, file, fileFullPath);
            });
            
            chaptersEl.appendChild(chapEl);
          });
          
          header.addEventListener('click', () => {
            volEl.classList.toggle('active');
          });
          
          volEl.appendChild(header);
          volEl.appendChild(chaptersEl);
          volumesList.appendChild(volEl);
        });

        updateProgressUI();
        renderCompletedIcons();
      })
      .catch(err => {
        volumesList.innerHTML = `<div style="color: var(--color-error); text-align: center; padding: 20px;">Không thể tải danh sách: ${err.message}</div>`;
      });
  }

  // Load Chapter Content (fetch the markdown file directly from the repo)
  function loadChapter(volume, filename, fullPath) {
    currentVolume = volume;
    currentChapter = filename;
    currentFilePath = fullPath;
    
    // Close quiz drawer if open when switching chapters
    closeQuizDrawer();

    activePath.innerHTML = `<span>${volume.replace(/-/g, ' ')}</span> <span class="path-separator">/</span> <span class="path-active">${filename.replace(/-/g, ' ').replace('.md', '')}</span>`;
    
    markdownSection.innerHTML = '<div class="loading-spinner" style="margin: 100px auto;"></div>';
    completeBtnContainer.style.display = 'none';
    openQuizBtn.style.display = 'none';
    
    resetQuizArea();

    // Fetch markdown file directly using relative path
    fetch(`./${fullPath}`)
      .then(res => {
        if (!res.ok) throw new Error('Không thể tải bài giảng');
        return res.text();
      })
      .then(markdownText => {
        // Render Markdown content
        markdownSection.innerHTML = marked.parse(markdownText);
        
        // Highlight code syntax
        markdownSection.querySelectorAll('pre code').forEach((block) => {
          hljs.highlightElement(block);
        });

        // Render LaTeX math formulas
        if (typeof renderMathInElement === 'function') {
          renderMathInElement(markdownSection, {
            delimiters: [
              {left: '$$', right: '$$', display: true},
              {left: '$', right: '$', display: false},
              {left: '\\(', right: '\\)', display: false},
              {left: '\\[', right: '\\]', display: true}
            ],
            throwOnError: false
          });
        }

        // Setup Complete Button State
        const completed = getCompletedChapters();
        if (completed.includes(fullPath)) {
          markCompleteBtn.textContent = '✓ Đã hoàn thành chương';
          markCompleteBtn.classList.add('completed');
        } else {
          markCompleteBtn.textContent = '✓ Đánh dấu đã học xong chương này';
          markCompleteBtn.classList.remove('completed');
        }
        completeBtnContainer.style.display = 'flex';

        // Enable Quiz Drawer button
        openQuizBtn.style.display = 'block';
        setupQuizTrigger();
      })
      .catch(err => {
        markdownSection.innerHTML = `<div style="color: var(--color-error); padding: 40px;">Lỗi tải bài giảng: ${err.message}</div>`;
      });
  }

  function resetQuizArea() {
    quizArea.innerHTML = `
      <div class="empty-quiz-state" style="padding: 8px 0; align-items: flex-start; text-align: left;">
        <span style="font-size: 13.5px; line-height: 1.6; color: var(--text-primary); font-weight: 500; margin-bottom: 8px;">Cổng kiểm duyệt đề thi thông minh của tập đoàn đã sẵn sàng. Vui lòng cấu hình các tham số đề thi dưới đây:</span>
        
        <div style="width: 100%; display: flex; flex-direction: column; gap: 14px; margin-top: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
            <label style="font-size: 12px; font-weight: 600; color: var(--text-secondary); letter-spacing: 0.05em;">MỨC ĐỘ KHÓ:</label>
            <select id="quiz-difficulty" style="background: #ffffff; border: 1px solid var(--border-color); padding: 6px 12px; border-radius: 6px; font-size: 12.5px; outline: none; cursor: pointer; color: var(--text-primary); font-weight: 500;">
              <option value="easy">Dễ (Nhận biết)</option>
              <option value="medium" selected>Trung bình (Thông hiểu)</option>
              <option value="hard">Khó (Vận dụng nâng cao)</option>
            </select>
          </div>
          
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
            <label style="font-size: 12px; font-weight: 600; color: var(--text-secondary); letter-spacing: 0.05em;">SỐ CÂU HỎI:</label>
            <select id="quiz-limit" style="background: #ffffff; border: 1px solid var(--border-color); padding: 6px 12px; border-radius: 6px; font-size: 12.5px; outline: none; cursor: pointer; color: var(--text-primary); font-weight: 500;">
              <option value="3">3 câu</option>
              <option value="5" selected>5 câu</option>
              <option value="10">10 câu</option>
              <option value="15">15 câu</option>
              <option value="20">20 câu</option>
              <option value="30">30 câu (Tối đa)</option>
            </select>
          </div>
        </div>
        
        <button class="generate-quiz-btn" id="generate-quiz-btn" style="margin-top: 24px; width: 100%;">✏️ Tạo câu hỏi trắc nghiệm</button>
      </div>
    `;
  }

  function setupQuizTrigger() {
    const btn = document.getElementById('generate-quiz-btn');
    if (btn) {
      btn.addEventListener('click', generateQuiz);
    }
  }

  // Request Gemini API to generate Quiz directly from the client (Serverless)
  function generateQuiz() {
    const apiKey = localStorage.getItem('gemini_api_key');
    if (!apiKey) {
      alert('Vui lòng click nút "Gemini Key" ở góc trên để cấu hình API Key trước khi tạo trắc nghiệm!');
      configModal.style.display = 'flex';
      return;
    }

    const diffEl = document.getElementById('quiz-difficulty');
    const limitEl = document.getElementById('quiz-limit');
    
    if (diffEl) lastSelectedDifficulty = diffEl.value;
    if (limitEl) lastSelectedLimit = parseInt(limitEl.value, 10);

    const friendlyDiff = lastSelectedDifficulty === 'easy' ? 'Dễ' : lastSelectedDifficulty === 'hard' ? 'Khó' : 'Trung bình';

    quizArea.innerHTML = `
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; height: 100%; min-height: 200px; padding: 0 10px; width: 100%;">
        <div class="loading-spinner"></div>
        <span style="color: var(--text-secondary); font-size: 12.5px; text-align: center; line-height: 1.5;">
          Gemini đang phân tích bài giảng và biên soạn ${lastSelectedLimit} câu hỏi trắc nghiệm (${friendlyDiff})...
        </span>
        <div style="width: 100%; height: 6px; background: #e7e7e4; border-radius: 4px; overflow: hidden; margin-top: 8px; position: relative;">
          <div id="quiz-progress-bar" style="width: 0%; height: 100%; background: var(--color-accent); border-radius: 4px; transition: width 0.2s ease-out;"></div>
        </div>
        <span id="quiz-progress-text" style="font-size: 11px; color: var(--text-muted); font-weight: 500;">Đang khởi tạo kết nối... 0%</span>
      </div>
    `;

    // Start progress simulation based on selected limit
    let progress = 0;
    const estimatedDuration = 2000 + lastSelectedLimit * 500; // time depends on question count
    const intervalTime = 100;
    const increment = 95 / (estimatedDuration / intervalTime);

    const progressInterval = setInterval(() => {
      progress = Math.min(95, progress + increment);
      const progressBar = document.getElementById('quiz-progress-bar');
      const progressText = document.getElementById('quiz-progress-text');
      if (progressBar) progressBar.style.width = `${Math.round(progress)}%`;
      if (progressText) {
        if (progress < 25) {
          progressText.textContent = `Đang đọc nội dung bài học... ${Math.round(progress)}%`;
        } else if (progress < 60) {
          progressText.textContent = `Gemini đang biên soạn đề thi... ${Math.round(progress)}%`;
        } else if (progress < 85) {
          progressText.textContent = `Đang tối ưu cấu trúc đáp án... ${Math.round(progress)}%`;
        } else {
          progressText.textContent = `Đang đóng gói dữ liệu phản hồi... ${Math.round(progress)}%`;
        }
      }
    }, intervalTime);

    // Fetch the raw text of the markdown file to send in the prompt
    fetch(`./${currentFilePath}`)
      .then(res => {
        if (!res.ok) throw new Error('Không thể đọc bài giảng để gửi prompt');
        return res.text();
      })
      .then(markdownContent => {
        const diffText = {
          "easy": "DỄ (nhận biết trực tiếp kiến thức trong bài giảng, các câu hỏi cơ bản)",
          "medium": "TRUNG BÌNH (thông hiểu và áp dụng, đòi hỏi phân tích nhẹ)",
          "hard": "KHÓ (phân tích sâu, suy luận logic, giải quyết tình huống thực tế phức tạp)"
        }[lastSelectedDifficulty] || "TRUNG BÌNH";

        const prompt = `Dưới đây là nội dung bài giảng của một chương trong tài liệu 'AI Automation Engineer Playbook'.
Nhiệm vụ của bạn là biên soạn đúng chính xác ${lastSelectedLimit} câu hỏi trắc nghiệm tiếng Việt chất lượng cao với mức độ khó: ${diffText} để kiểm tra mức độ hiểu bài của học sinh dựa trên nội dung này.

Yêu cầu kỹ thuật:
1. Mỗi câu hỏi phải có chính xác 4 lựa chọn (A, B, C, D).
2. Phải có 1 chỉ thị correct_index (số nguyên từ 0 đến 3) đại diện cho đáp án đúng.
3. Phải cung cấp phần 'explanation' (giải thích ngắn gọn vì sao đáp án đó đúng và các đáp án khác sai dựa trên nội dung bài giảng).
4. Quy định nghiêm ngặt về cấu trúc đáp án để đảm bảo tính phân loại và đòi hỏi tư duy cao:
   - Cả 4 lựa chọn (A, B, C, D) phải có độ dài tương đồng nhau, viết cùng một cấu trúc ngữ pháp và mức độ chi tiết như nhau. Tuyệt đối KHÔNG được để đáp án đúng dài hơn hoặc chi tiết hơn hẳn các đáp án sai.
   - Các đáp án sai (phương án nhiễu) phải cực kỳ tương đồng về mặt từ ngữ, thuật ngữ và cấu trúc với đáp án đúng, chỉ khác biệt rất ít ở các chi tiết kỹ thuật cốt lõi (ví dụ: đổi tên hàm, thay đổi logic tham số, hoặc đảo ngược nguyên lý hoạt động). Học sinh phải đọc kỹ và phân tích sâu sắc mới phân biệt được.
5. Bạn BẮT BUỘC phải trả về dữ liệu đúng cấu trúc JSON định hình sau:
{
  "questions": [
    {
      "question": "Câu hỏi số 1...",
      "options": ["Lựa chọn A", "Lựa chọn B", "Lựa chọn C", "Lựa chọn D"],
      "correct_index": 0,
      "explanation": "Giải thích chi tiết..."
    }
  ]
}

Nội dung bài giảng chương:
${markdownContent}
`;

        // Direct client-side fetch call to Google Gemini API
        return fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            contents: [{
              parts: [{ text: prompt }]
            }],
            generationConfig: {
              responseMimeType: "application/json"
            }
          })
        });
      })
      .then(res => {
        if (!res.ok) {
          return res.json().then(err => {
            throw new Error((err.error && err.error.message) || 'Lỗi gọi API từ Google Studio');
          });
        }
        return res.json();
      })
      .then(data => {
        clearInterval(progressInterval);
        
        // Show 100% completed state before rendering questions
        const progressBar = document.getElementById('quiz-progress-bar');
        const progressText = document.getElementById('quiz-progress-text');
        if (progressBar) progressBar.style.width = '100%';
        if (progressText) progressText.textContent = 'Hoàn tất biên soạn! 100%';

        setTimeout(() => {
          try {
            const rawText = data.candidates[0].content.parts[0].text;
            const quizData = JSON.parse(rawText);
            renderQuiz(quizData.questions);
          } catch (parseErr) {
            throw new Error('Lỗi phân tích cú pháp JSON trả về từ Gemini: ' + parseErr.message);
          }
        }, 200);
      })
      .catch(err => {
        clearInterval(progressInterval);
        quizArea.innerHTML = `
          <div style="color: var(--color-error); text-align: center; padding: 20px;">
            <p>Lỗi tạo trắc nghiệm: ${err.message}</p>
            <button class="generate-quiz-btn" id="generate-quiz-btn" style="margin-top: 16px; width: 100%;">Thử lại</button>
          </div>
        `;
        setupQuizTrigger();
      });
  }

  // Render Quiz cards
  function renderQuiz(questions) {
    quizArea.innerHTML = '';
    
    const quizContainer = document.createElement('div');
    quizContainer.className = 'quiz-container';

    const topBar = document.createElement('div');
    topBar.style.display = 'flex';
    topBar.style.justifyContent = 'space-between';
    topBar.style.alignItems = 'center';
    topBar.style.marginBottom = '12px';
    
    const friendlyDiff = lastSelectedDifficulty === 'easy' ? 'Dễ' : lastSelectedDifficulty === 'hard' ? 'Khó' : 'Trung bình';
    topBar.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 2px;">
        <h3 class="quiz-title" style="font-size:14px; font-weight:700;">Đề khảo sát</h3>
        <span style="font-size: 11px; color: var(--text-secondary);">${friendlyDiff} • ${lastSelectedLimit} câu</span>
      </div>
    `;
    
    const btnGroup = document.createElement('div');
    btnGroup.className = 'quiz-btn-group';

    const changeConfigBtn = document.createElement('button');
    changeConfigBtn.className = 'quiz-btn-outline';
    changeConfigBtn.textContent = 'Đổi đề';
    changeConfigBtn.addEventListener('click', () => {
      resetQuizArea();
      setupQuizTrigger();
    });
    btnGroup.appendChild(changeConfigBtn);
    
    const regenBtn = document.createElement('button');
    regenBtn.className = 'quiz-btn-solid';
    regenBtn.textContent = 'Tạo lại';
    regenBtn.addEventListener('click', generateQuiz);
    btnGroup.appendChild(regenBtn);
    
    topBar.appendChild(btnGroup);
    quizContainer.appendChild(topBar);

    questions.forEach((q, qIndex) => {
      const card = document.createElement('div');
      card.className = 'quiz-card';
      
      const questionEl = document.createElement('div');
      questionEl.className = 'question-text';
      questionEl.textContent = `Câu ${qIndex + 1}: ${q.question}`;
      card.appendChild(questionEl);
      
      const optionsList = document.createElement('div');
      optionsList.className = 'options-list';
      
      const optionLetters = ['A', 'B', 'C', 'D'];
      let answered = false;

      q.options.forEach((opt, optIndex) => {
        const optionItem = document.createElement('div');
        optionItem.className = 'option-item';
        optionItem.innerHTML = `<span class="option-letter">${optionLetters[optIndex]}.</span> <span>${opt}</span>`;
        
        optionItem.addEventListener('click', () => {
          if (answered) return;
          answered = true;
          
          optionItem.classList.add('selected');
          const isCorrect = optIndex === q.correct_index;
          
          optionsList.querySelectorAll('.option-item').forEach((item, index) => {
            if (index === q.correct_index) {
              item.classList.add('correct');
            } else if (index === optIndex && !isCorrect) {
              item.classList.add('incorrect');
            }
          });
          
          expPanel.style.display = 'block';
        });
        
        optionsList.appendChild(optionItem);
      });
      
      card.appendChild(optionsList);
      
      const expPanel = document.createElement('div');
      expPanel.className = 'explanation-panel';
      expPanel.innerHTML = `<strong>💡 Giải thích:</strong> ${q.explanation}`;
      card.appendChild(expPanel);

      quizContainer.appendChild(card);
    });

    quizArea.appendChild(quizContainer);
  }

  // Init
  loadSidebar();
});
