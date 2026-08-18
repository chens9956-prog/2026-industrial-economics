import json

with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\questions_data.json', 'r', encoding='utf-8') as f:
    q_data = json.load(f)

js_content = f"""// Online Exam System JavaScript Logic with Top & Bottom Score Display & Dark/Light Theme Switch

const cleanStr = (str) => (str || '').toString().trim().replace(/[\\s\\uFEFF\\xA0]+/g, '');

document.addEventListener('DOMContentLoaded', () => {{

    // --- Built-in Authorized Student Roster ---
    const defaultRoster = [
        {{ id: '2026010001', name: '高建刚' }},
        {{ id: '2026010002', name: '李明' }},
        {{ id: '2026010003', name: '王芳' }}
    ];

    // --- 50 Questions Bank (Chapters 1-10, 2 pts each, Total 100 pts) ---
    const questionBank = {json.dumps(q_data, ensure_ascii=False, indent=4)};

    // --- State ---
    let currentStudent = {{ id: '', name: '' }};
    let userAnswers = {{}};
    let timerInterval = null;
    let timeRemaining = 75 * 60; // 75 minutes in seconds
    let timeElapsed = 0;
    let autoCloseTimer = null;

    // --- Theme Toggle Logic ---
    const btnToggleTheme = document.getElementById('btn-toggle-theme');
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');

    const applyTheme = (theme) => {{
        if (theme === 'light') {{
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light-mode');
            document.body.classList.remove('bg-slate-950', 'text-slate-100');
            document.body.classList.add('bg-slate-100', 'text-slate-900');
            if (themeIcon) themeIcon.className = 'fa-solid fa-sun text-amber-500';
            if (themeText) themeText.textContent = '浅色模式';
        }} else {{
            document.documentElement.classList.remove('light-mode');
            document.documentElement.classList.add('dark');
            document.body.classList.remove('bg-slate-100', 'text-slate-900');
            document.body.classList.add('bg-slate-950', 'text-slate-100');
            if (themeIcon) themeIcon.className = 'fa-solid fa-moon text-sky-400';
            if (themeText) themeText.textContent = '深色模式';
        }}
    }};

    const savedTheme = localStorage.getItem('theme_mode') || 'dark';
    applyTheme(savedTheme);

    if (btnToggleTheme) {{
        btnToggleTheme.addEventListener('click', () => {{
            const currentTheme = localStorage.getItem('theme_mode') === 'light' ? 'dark' : 'light';
            localStorage.setItem('theme_mode', currentTheme);
            applyTheme(currentTheme);
        }});
    }}

    // --- Storage Helpers ---
    const getStudentRoster = () => {{
        const saved = localStorage.getItem('student_roster_v1');
        let list = saved ? JSON.parse(saved) : defaultRoster;
        defaultRoster.forEach(def => {{
            const exists = list.some(item => cleanStr(item.id) === cleanStr(def.id) && cleanStr(item.name) === cleanStr(def.name));
            if (!exists) list.unshift(def);
        }});
        return list;
    }};

    const getSubmissions = () => {{
        return JSON.parse(localStorage.getItem('exam_submissions_v1') || '[]');
    }};

    const saveSubmissionRecord = (record) => {{
        const records = getSubmissions();
        const existingIdx = records.findIndex(item => cleanStr(item.id) === cleanStr(record.id));
        if (existingIdx >= 0) {{
            records[existingIdx] = {{ ...records[existingIdx], ...record }};
        }} else {{
            records.unshift(record);
        }}
        localStorage.setItem('exam_submissions_v1', JSON.stringify(records));
    }};

    // --- DOM Elements ---
    const viewLogin = document.getElementById('view-login');
    const viewExam = document.getElementById('view-exam');
    const viewResult = document.getElementById('view-result');

    const formLogin = document.getElementById('form-login');
    const inputStudentId = document.getElementById('input-student-id');
    const inputStudentName = document.getElementById('input-student-name');
    const loginErrorMsg = document.getElementById('login-error-msg');
    const loginErrorText = document.getElementById('login-error-text');

    const alreadySubmittedMsg = document.getElementById('already-submitted-msg');
    const alreadySubmittedDetail = document.getElementById('already-submitted-detail');
    const closeCountdownTimer = document.getElementById('close-countdown-timer');
    const btnLoginSubmit = document.getElementById('btn-login-submit');

    const examStudentInfo = document.getElementById('exam-student-info');
    const examProgressText = document.getElementById('exam-progress-text');
    const examTimer = document.getElementById('exam-timer');
    const questionsContainer = document.getElementById('questions-container');
    const btnSubmitExam = document.getElementById('btn-submit-exam');
    const btnExitExam = document.getElementById('btn-exit-exam');
    const btnExitExamBottom = document.getElementById('btn-exit-exam-bottom');

    // Dual Score Display Elements (Top & Bottom)
    const resultScoreTop = document.getElementById('result-score-top');
    const resultAccuracyTop = document.getElementById('result-accuracy-top');
    const resultDurationTop = document.getElementById('result-duration-top');

    const resultScore = document.getElementById('result-score');
    const resultAccuracy = document.getElementById('result-accuracy');
    const resultDuration = document.getElementById('result-duration');

    const resultDetailsContainer = document.getElementById('result-details-container');
    const oneTimeCheckNotice = document.getElementById('one-time-check-notice');
    const queryChanceBadge = document.getElementById('query-chance-badge');
    const queryCountdownTimer = document.getElementById('query-countdown-timer');
    const resultStatusTag = document.getElementById('result-status-tag');
    const btnRestartStudent = document.getElementById('btn-restart-student');

    // --- View Navigation Helper ---
    const showView = (viewToShow) => {{
        [viewLogin, viewExam, viewResult].forEach(v => {{
            if (v) v.classList.add('hidden');
        }});
        if (viewToShow) viewToShow.classList.remove('hidden');
    }};

    // --- Exit Exam Action ---
    const handleExitExam = () => {{
        if (confirm('确定要退出本次随堂考试吗？已作答的选项将被清空，您可稍后再重新登录作答。')) {{
            if (timerInterval) clearInterval(timerInterval);
            userAnswers = {{}};
            currentStudent = {{ id: '', name: '' }};
            inputStudentId.value = '';
            inputStudentName.value = '';
            loginErrorMsg.classList.add('hidden');
            alreadySubmittedMsg.classList.add('hidden');
            showView(viewLogin);
        }}
    }};

    if (btnExitExam) btnExitExam.addEventListener('click', handleExitExam);
    if (btnExitExamBottom) btnExitExamBottom.addEventListener('click', handleExitExam);

    // --- Student Login & 2-Time 15s Query Chance Logic ---
    formLogin.addEventListener('submit', (e) => {{
        e.preventDefault();
        loginErrorMsg.classList.add('hidden');
        alreadySubmittedMsg.classList.add('hidden');

        const studentId = cleanStr(inputStudentId.value);
        const studentName = cleanStr(inputStudentName.value);

        if (!studentId || !studentName) {{
            loginErrorText.textContent = '请完整填写学号和姓名！';
            loginErrorMsg.classList.remove('hidden');
            return;
        }}

        // 1. Roster Match Check
        const currentRoster = getStudentRoster();
        const matched = currentRoster.find(s => cleanStr(s.id) === studentId && cleanStr(s.name) === studentName);

        if (!matched) {{
            loginErrorText.textContent = '学号与姓名不匹配，或您不在允许考试的学生名单中，请核实后再试。';
            loginErrorMsg.classList.remove('hidden');
            return;
        }}

        // 2. Check Submission Status & 2-Time Query Limit
        const submissions = getSubmissions();
        const existingRecord = submissions.find(r => cleanStr(r.id) === studentId);

        if (existingRecord) {{
            let checkCount = existingRecord.scoreCheckedCount || 0;

            if (checkCount >= 2) {{
                triggerRepeatSubmissionLock(studentId, matched.name, existingRecord.timestamp);
                return;
            }} else {{
                checkCount += 1;
                existingRecord.scoreCheckedCount = checkCount;
                saveSubmissionRecord(existingRecord);

                renderReadOnlyScoreResult(existingRecord, checkCount);
                return;
            }}
        }}

        // 3. First-time Login -> Start Exam
        currentStudent = {{ id: studentId, name: studentName }};
        userAnswers = {{}};
        timeRemaining = 75 * 60; // 75 minutes
        timeElapsed = 0;

        examStudentInfo.textContent = `${{studentId}} - ${{studentName}}`;
        renderQuestions();
        showView(viewExam);
        startTimer();
    }});

    // --- Render Read-Only Score Query Page with Dual Score Display ---
    const renderReadOnlyScoreResult = (record, checkCount = 1) => {{
        // Top score card
        if (resultScoreTop) resultScoreTop.textContent = record.score;
        if (resultAccuracyTop) resultAccuracyTop.textContent = record.accuracy;
        if (resultDurationTop) resultDurationTop.textContent = `用时 ${{record.duration}}`;

        // Bottom score card
        resultScore.textContent = record.score;
        resultAccuracy.textContent = record.accuracy;
        resultDuration.textContent = `用时 ${{record.duration}}`;

        // Show 2-Time Query Chance Banner
        if (checkCount > 0) {{
            oneTimeCheckNotice.classList.remove('hidden');
            queryChanceBadge.textContent = `【查分模式 · 第 ${{checkCount}}/2 次】`;
            resultStatusTag.textContent = `考生：${{record.id}} - ${{record.name}} | 查分模式（只读无法修改答案）`;
        }} else {{
            oneTimeCheckNotice.classList.add('hidden');
            resultStatusTag.textContent = '考案结果已成功保存并同步给教师后台';
        }}

        // Render Question Breakdown
        const userSavedAns = record.userAnswers || {{}};
        resultDetailsContainer.innerHTML = questionBank.map((q, idx) => {{
            const userAns = userSavedAns[q.id] || '未作答';
            const isCorrect = userAns === q.answer;

            return `
                <div class="p-4 sm:p-5 rounded-2xl bg-slate-950 dark:bg-slate-950 border ${{isCorrect ? 'border-emerald-500/40' : 'border-rose-500/40'}} space-y-2">
                    <div class="flex items-center justify-between text-xs font-bold">
                        <span class="text-slate-300 font-mono">第 ${{idx + 1}} 题 / 共 50 题【${{q.chapter}} · 2分】</span>
                        <span class="${{isCorrect ? 'text-emerald-400' : 'text-rose-400'}} font-mono">
                            ${{isCorrect ? '<i class="fa-solid fa-check mr-1"></i>回答正确 (+2分)' : '<i class="fa-solid fa-xmark mr-1"></i>回答错误 (0分)'}}
                        </span>
                    </div>
                    <p class="text-sm font-semibold text-white">${{q.title}}</p>
                    <div class="text-xs font-mono space-y-1 pt-1">
                        <p class="text-slate-400">您的选择：<span class="${{isCorrect ? 'text-emerald-400 font-bold' : 'text-rose-400 font-bold'}}">${{userAns}}</span></p>
                        <p class="text-slate-400">正确答案：<span class="text-emerald-400 font-bold">${{q.answer}}</span></p>
                    </div>
                    <div class="text-xs text-slate-400 bg-slate-900/80 p-3 rounded-xl border border-slate-800/80 mt-2">
                        <strong class="text-sky-400">解析：</strong>${{q.explanation}}
                    </div>
                </div>
            `;
        }}).join('');

        showView(viewResult);
        window.scrollTo({{ top: 0, behavior: 'smooth' }});

        if (checkCount > 0) {{
            let querySecondsLeft = 15;
            if (queryCountdownTimer) queryCountdownTimer.textContent = querySecondsLeft;

            if (autoCloseTimer) clearInterval(autoCloseTimer);
            autoCloseTimer = setInterval(() => {{
                querySecondsLeft--;
                if (queryCountdownTimer) queryCountdownTimer.textContent = querySecondsLeft;

                if (querySecondsLeft <= 0) {{
                    clearInterval(autoCloseTimer);
                    try {{
                        window.close();
                    }} catch (err) {{}}

                    window.location.reload();
                }}
            }}, 1000);
        }}
    }};

    // --- Trigger 15-Second Countdown Lock for Exceeded Query Limit ---
    const triggerRepeatSubmissionLock = (studentId, studentName, timestamp) => {{
        alreadySubmittedDetail.innerHTML = `学号 [<strong>${{studentId}}</strong>] <strong>${{studentName}}</strong> 的试卷已于 <span class="font-mono text-amber-300">${{timestamp || '稍早前'}}</span> 提交保存，且您已使用完全部 <strong>2 次查分机会</strong>。<br>为了防止替考与重复查分，系统将在 <strong>15 秒</strong> 后自动关闭！`;
        alreadySubmittedMsg.classList.remove('hidden');
        
        inputStudentId.disabled = true;
        inputStudentName.disabled = true;
        btnLoginSubmit.disabled = true;
        btnLoginSubmit.classList.add('opacity-50', 'cursor-not-allowed');

        let secondsLeft = 15;
        closeCountdownTimer.textContent = secondsLeft;

        if (autoCloseTimer) clearInterval(autoCloseTimer);
        autoCloseTimer = setInterval(() => {{
            secondsLeft--;
            closeCountdownTimer.textContent = secondsLeft;

            if (secondsLeft <= 0) {{
                clearInterval(autoCloseTimer);
                try {{
                    window.close();
                }} catch (err) {{}}
                
                document.body.innerHTML = `
                    <div class="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6 text-center space-y-4">
                        <div class="w-16 h-16 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30 flex items-center justify-center text-2xl font-bold">
                            <i class="fa-solid fa-lock"></i>
                        </div>
                        <h2 class="text-2xl font-extrabold text-white">系统已锁定并关闭</h2>
                        <p class="text-xs text-slate-400 max-w-sm">学号 [${{studentId}}] ${{studentName}} 的 2 次查分机会已全部用尽。试卷记录已存入教师后台。</p>
                        <a href="index.html" class="px-4 py-2 rounded-xl bg-slate-800 text-sky-400 text-xs font-semibold border border-slate-700">重新加载页面</a>
                    </div>
                `;
            }}
        }}, 1000);
    }};

    // --- Render 50 Exam Questions ---
    const renderQuestions = () => {{
        questionsContainer.innerHTML = questionBank.map((q, idx) => `
            <div class="question-card bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-4">
                <div class="flex items-start justify-between gap-3">
                    <div class="flex items-center gap-2">
                        <span class="w-7 h-7 rounded-xl bg-sky-500/20 text-sky-400 border border-sky-500/30 flex items-center justify-center font-bold font-mono text-xs">
                            ${{idx + 1}}
                        </span>
                        <span class="text-xs text-slate-400 font-semibold">【${{q.chapter}} · 单选题 · 2分】</span>
                    </div>
                </div>

                <h3 class="text-base sm:text-lg font-bold text-white leading-relaxed">
                    ${{q.title}}
                </h3>

                <!-- Options -->
                <div class="space-y-2.5 pt-2">
                    ${{q.options.map(opt => `
                        <div data-qid="${{q.id}}" data-key="${{opt.key}}" class="quiz-option p-4 rounded-2xl bg-slate-950 border border-slate-800/80 cursor-pointer flex items-center gap-3 text-sm text-slate-200">
                            <span class="w-6 h-6 rounded-lg bg-slate-800 text-slate-300 font-bold font-mono text-xs flex items-center justify-center border border-slate-700 option-badge">
                                ${{opt.key}}
                            </span>
                            <span>${{opt.text}}</span>
                        </div>
                    `).join('')}}
                </div>
            </div>
        `).join('');

        document.querySelectorAll('.quiz-option').forEach(optionEl => {{
            optionEl.addEventListener('click', () => {{
                const qid = optionEl.getAttribute('data-qid');
                const key = optionEl.getAttribute('data-key');
                userAnswers[qid] = key;

                const siblingOptions = document.querySelectorAll(`.quiz-option[data-qid="${{qid}}"]`);
                siblingOptions.forEach(opt => {{
                    opt.classList.remove('selected');
                    opt.querySelector('.option-badge').classList.remove('bg-sky-500', 'text-white', 'border-sky-400');
                }});

                optionEl.classList.add('selected');
                optionEl.querySelector('.option-badge').classList.add('bg-sky-500', 'text-white', 'border-sky-400');

                const answeredCount = Object.keys(userAnswers).length;
                examProgressText.textContent = `${{answeredCount}} / ${{questionBank.length}}`;
            }});
        }});

        examProgressText.textContent = `0 / ${{questionBank.length}}`;
    }};

    // --- Timer Logic (75 mins = 4500 secs) ---
    const startTimer = () => {{
        if (timerInterval) clearInterval(timerInterval);
        updateTimerDisplay();

        timerInterval = setInterval(() => {{
            timeRemaining--;
            timeElapsed++;
            updateTimerDisplay();

            if (timeRemaining <= 0) {{
                clearInterval(timerInterval);
                alert('考试时间到（75分钟），系统已为您自动交卷！');
                submitExam();
            }}
        }}, 1000);
    }};

    const updateTimerDisplay = () => {{
        const mins = Math.floor(timeRemaining / 60);
        const secs = timeRemaining % 60;
        examTimer.textContent = `${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;
    }};

    // --- Submit Exam (50 questions * 2 pts = 100 pts) ---
    btnSubmitExam.addEventListener('click', () => {{
        const answeredCount = Object.keys(userAnswers).length;
        if (answeredCount < questionBank.length) {{
            if (!confirm(`您还有 ${{questionBank.length - answeredCount}} 道题未作答，确定要现在交卷吗？`)) {{
                return;
            }}
        }}
        submitExam();
    }});

    const submitExam = () => {{
        if (timerInterval) clearInterval(timerInterval);

        let correctCount = 0;
        questionBank.forEach(q => {{
            if (userAnswers[q.id] === q.answer) {{
                correctCount++;
            }}
        }});

        const totalScore = correctCount * 2;
        const accuracy = Math.round((correctCount / questionBank.length) * 100);
        const durationMin = Math.floor(timeElapsed / 60);
        const durationSec = timeElapsed % 60;
        const durationStr = `${{String(durationMin).padStart(2, '0')}}:${{String(durationSec).padStart(2, '0')}}`;

        const newRecord = {{
            id: currentStudent.id,
            name: currentStudent.name,
            score: totalScore,
            accuracy: `${{accuracy}}%`,
            duration: durationStr,
            userAnswers: {{ ...userAnswers }},
            scoreCheckedCount: 0,
            timestamp: new Date().toLocaleString('zh-CN', {{ hour12: false }})
        }};

        saveSubmissionRecord(newRecord);
        renderReadOnlyScoreResult(newRecord, 0);
    }};

    btnRestartStudent.addEventListener('click', () => {{
        window.location.reload();
    }});

}});
"""

with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\app.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updated app.js successfully with Dual Score Display & Theme Toggle!")
