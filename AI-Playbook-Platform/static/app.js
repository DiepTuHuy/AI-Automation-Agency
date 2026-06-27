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
    fetch('/api/config')
      .then(res => res.json())
      .then(data => {
        if (data.key_configured) {
          apiKeyInput.placeholder = '••••••••••••••••••••••••';
        }
      });
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
    fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gemini_api_key: key })
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          alert('Đã lưu cấu hình API Key thành công!');
          configModal.style.display = 'none';
          apiKeyInput.value = '';
        } else {
          alert('Lỗi lưu cấu hình: ' + data.detail);
        }
      });
  });

  // Quiz Drawer Toggling
  openQuizBtn.addEventListener('click', () => {
    document.body.classList.add('quiz-open');
  });

  function closeQuizDrawer() {
    document.body.classList.remove('quiz-open');
  }

  closeQuizBtn.addEventListener('click', closeQuizDrawer);
  drawerBackdrop.addEventListener('click', closeQuizDrawer);

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

  // Load sidebar data
  function loadSidebar() {
    fetch('/api/volumes')
      .then(res => res.json())
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
        volumesList.innerHTML = `<div style="color: var(--color-error); text-align: center; padding: 20px;">Không thể tải danh sách: ${err}</div>`;
      });
  }

  // Load Chapter Content
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

    fetch(`/api/content?path=${encodeURIComponent(fullPath)}`)
      .then(res => {
        if (!res.ok) throw new Error('Không thể đọc file');
        return res.json();
      })
      .then(data => {
        // Render Markdown content
        markdownSection.innerHTML = marked.parse(data.content);
        
        // Highlight code syntax
        markdownSection.querySelectorAll('pre code').forEach((block) => {
          hljs.highlightElement(block);
        });

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

  // Request Gemini API to generate Quiz
  function generateQuiz() {
    const diffEl = document.getElementById('quiz-difficulty');
    const limitEl = document.getElementById('quiz-limit');
    
    if (diffEl) lastSelectedDifficulty = diffEl.value;
    if (limitEl) lastSelectedLimit = parseInt(limitEl.value, 10);

    quizArea.innerHTML = `
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; height: 100%; min-height: 200px;">
        <div class="loading-spinner"></div>
        <span style="color: var(--text-secondary); font-size: 12.5px; text-align: center; line-height: 1.5;">Gemini đang phân tích bài giảng và biên soạn ${lastSelectedLimit} câu hỏi trắc nghiệm (${lastSelectedDifficulty === 'easy' ? 'Dễ' : lastSelectedDifficulty === 'hard' ? 'Khó' : 'Trung bình'})...</span>
      </div>
    `;

    fetch(`/api/quiz?path=${encodeURIComponent(currentFilePath)}&difficulty=${lastSelectedDifficulty}&limit=${lastSelectedLimit}`)
      .then(res => {
        if (!res.ok) {
          return res.json().then(err => { throw new Error(err.detail || 'Không thể tạo quiz'); });
        }
        return res.json();
      })
      .then(data => {
        renderQuiz(data.questions);
      })
      .catch(err => {
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
    btnGroup.style.display = 'flex';
    btnGroup.style.gap = '6px';

    const changeConfigBtn = document.createElement('button');
    changeConfigBtn.className = 'btn-secondary';
    changeConfigBtn.style.fontSize = '11px';
    changeConfigBtn.style.padding = '4px 10px';
    changeConfigBtn.textContent = '⚙️ Đổi đề';
    changeConfigBtn.addEventListener('click', () => {
      resetQuizArea();
      setupQuizTrigger();
    });
    btnGroup.appendChild(changeConfigBtn);
    
    const regenBtn = document.createElement('button');
    regenBtn.className = 'btn-secondary';
    regenBtn.style.fontSize = '11px';
    regenBtn.style.padding = '4px 10px';
    regenBtn.textContent = '🔄 Tạo lại';
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
        optionItem.innerHTML = `<span class="option-letter">${optionLetters[optIndex]}</span> <span>${opt}</span>`;
        
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
