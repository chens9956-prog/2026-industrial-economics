import json

with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\questions_data.json', 'r', encoding='utf-8') as f:
    questions_json = f.read()

app_js_template = """// Online Exam System JavaScript Logic (60 Questions: 40 Single Choice @ 1.5 pts + 20 Multiple Choice @ 2.0 pts = 100 pts)

const cleanStr = (str) => (str || '').toString().trim().replace(/[\\s\\uFEFF\\xA0]+/g, '');

document.addEventListener('DOMContentLoaded', () => {

    // --- Built-in Authorized Student Roster ---
    const defaultRoster = [
        { id: '2026010001', name: '高建刚' },
        { id: '2026010002', name: '李明' },
        { id: '2026010003', name: '王芳' }
    ];

    // --- 60 Questions Bank ---
    const questionBank = REPLACE_QUESTIONS_JSON;

    // --- State ---
    let currentStudent = null;
    let userAnswers = {};
    let timeRemaining = 75 * 60;
    let timeElapsed = 0;
    let timerInterval = null;
    let autoCloseTimer = null;

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
    const btnToggleTheme = document.getElementById('btn-toggle-theme');
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');

    const examStudentInfo = document.getElementById('exam-student-info');
    const examTimer = document.getElementById('exam-timer');
    const examProgressText = document.getElementById('exam-progress-text');
    const questionsContainer = document.getElementById('questions-container');
    const btnSubmitExam = document.getElementById('btn-submit-exam');
    const btnExitExamHeader = document.getElementById('btn-exit-exam-header');
    const btnExitExamFooter = document.getElementById('btn-exit-exam-footer');

    const resultStudentInfo = document.getElementById('result-student-info');
    const resultScore = document.getElementById('result-score');
    const resultScoreTop = document.getElementById('result-score-top');
    const resultAccuracy = document.getElementById('result-accuracy');
    const resultDuration = document.getElementById('result-duration');
    const resultBreakdown = document.getElementById('result-breakdown');
    const btnRestartStudent = document.getElementById('btn-restart-student');
    const readOnlyQueryAlert = document.getElementById('read-only-query-alert');
    const readOnlyCountdown = document.getElementById('read-only-countdown');

    // --- Theme Switcher ---
    const applyTheme = (theme) => {
        if (theme === 'light') {
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light-mode');
            document.body.classList.remove('bg-slate-950', 'text-slate-100');
            document.body.classList.add('bg-slate-100', 'text-slate-900');
            if (themeIcon) themeIcon.className = 'fa-solid fa-sun text-amber-500';
            if (themeText) themeText.textContent = '浅色模式';
        } else {
            document.documentElement.classList.remove('light-mode');
            document.documentElement.classList.add('dark');
            document.body.classList.remove('bg-slate-100', 'text-slate-900');
            document.body.classList.add('bg-slate-950', 'text-slate-100');
            if (themeIcon) themeIcon.className = 'fa-solid fa-moon text-sky-400';
            if (themeText) themeText.textContent = '深色模式';
        }
    };

    const savedTheme = localStorage.getItem('theme_mode') || 'dark';
    applyTheme(savedTheme);

    if (btnToggleTheme) {
        btnToggleTheme.addEventListener('click', () => {
            const currentTheme = localStorage.getItem('theme_mode') === 'light' ? 'dark' : 'light';
            localStorage.setItem('theme_mode', currentTheme);
            applyTheme(currentTheme);
        });
    }

    const getStudentRoster = () => {
        const saved = localStorage.getItem('student_roster_v1');
        let list = saved ? JSON.parse(saved) : defaultRoster;
        defaultRoster.forEach(def => {
            const exists = list.some(item => cleanStr(item.id) === cleanStr(def.id) && cleanStr(item.name) === cleanStr(def.name));
            if (!exists) list.unshift(def);
        });
        return list;
    };

    const getSubmissions = () => JSON.parse(localStorage.getItem('exam_submissions_v1') || '[]');
    const saveSubmissionRecord = (record) => {
        let submissions = getSubmissions();
        const existingIdx = submissions.findIndex(r => cleanStr(r.id) === cleanStr(record.id));
        if (existingIdx >= 0) submissions[existingIdx] = record;
        else submissions.unshift(record);
        localStorage.setItem('exam_submissions_v1', JSON.stringify(submissions));
    };

    // --- Form Login Verification ---
    formLogin.addEventListener('submit', (e) => {
        e.preventDefault();
        loginErrorMsg.classList.add('hidden');
        alreadySubmittedMsg.classList.add('hidden');

        const sid = cleanStr(inputStudentId.value);
        const sname = cleanStr(inputStudentName.value);

        if (!sid || !sname) {
            loginErrorText.textContent = '请填写完整的学号与姓名！';
            loginErrorMsg.classList.remove('hidden');
            return;
        }

        const roster = getStudentRoster();
        const matchedStudent = roster.find(s => cleanStr(s.id) === sid && cleanStr(s.name) === sname);

        if (!matchedStudent) {
            loginErrorText.textContent = `学号 [${sid}] 与姓名 [${sname}] 不在授权考场名单中！`;
            loginErrorMsg.classList.remove('hidden');
            return;
        }

        const submissions = getSubmissions();
        const existingRecord = submissions.find(r => cleanStr(r.id) === sid);

        if (existingRecord) {
            let checkCount = existingRecord.scoreCheckedCount || 0;
            if (checkCount >= 2) {
                triggerRepeatSubmissionLock(sid, sname, existingRecord.timestamp);
                return;
            } else {
                checkCount += 1;
                existingRecord.scoreCheckedCount = checkCount;
                saveSubmissionRecord(existingRecord);
                renderReadOnlyScoreResult(existingRecord, checkCount);
                return;
            }
        }

        currentStudent = { id: sid, name: sname };
        examStudentInfo.textContent = `${sid} - ${sname}`;
        viewLogin.classList.add('hidden');
        viewExam.classList.remove('hidden');
        renderQuestions();
        startTimer();
    });

    const triggerRepeatSubmissionLock = (studentId, studentName, timestamp) => {
        alreadySubmittedDetail.innerHTML = `学号 [<strong>${studentId}</strong>] <strong>${studentName}</strong> 的试卷已于 <span class="font-mono text-amber-300">${timestamp || '稍早前'}</span> 提交保存，且您已使用完全部 <strong>2 次查分机会</strong>。<br>为了防止替考与重复查分，系统将在 <strong>15 秒</strong> 后自动关闭！`;
        alreadySubmittedMsg.classList.remove('hidden');
        inputStudentId.disabled = true;
        inputStudentName.disabled = true;
        btnLoginSubmit.disabled = true;
        btnLoginSubmit.classList.add('opacity-50', 'cursor-not-allowed');

        let secondsLeft = 15;
        closeCountdownTimer.textContent = secondsLeft;

        if (autoCloseTimer) clearInterval(autoCloseTimer);
        autoCloseTimer = setInterval(() => {
            secondsLeft--;
            closeCountdownTimer.textContent = secondsLeft;
            if (secondsLeft <= 0) {
                clearInterval(autoCloseTimer);
                try { window.close(); } catch (err) {}
                document.body.innerHTML = `
                    <div class="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6 text-center space-y-4">
                        <div class="w-16 h-16 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30 flex items-center justify-center text-2xl font-bold">
                            <i class="fa-solid fa-lock"></i>
                        </div>
                        <h2 class="text-2xl font-extrabold text-white">系统已锁定并关闭</h2>
                        <p class="text-xs text-slate-400 max-w-sm">学号 [${studentId}] ${studentName} 的 2 次查分机会已全部用尽。试卷记录已存入教师后台。</p>
                        <a href="index.html" class="px-4 py-2 rounded-xl bg-slate-800 text-sky-400 text-xs font-semibold border border-slate-700">重新加载页面</a>
                    </div>
                `;
            }
        }, 1000);
    };

    // --- Render 60 Questions (40 Single + 20 Multiple) ---
    const renderQuestions = () => {
        questionsContainer.innerHTML = questionBank.map((q, idx) => {
            const isMulti = q.type === 'multiple';
            const typeLabel = isMulti ? '多选题 · 2分' : '单选题 · 1.5分';
            const badgeColor = isMulti ? 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30' : 'bg-sky-500/20 text-sky-400 border-sky-500/30';

            return `
                <div class="question-card bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-4">
                    <div class="flex items-start justify-between gap-3">
                        <div class="flex items-center gap-2">
                            <span class="w-7 h-7 rounded-xl ${badgeColor} border flex items-center justify-center font-bold font-mono text-xs">
                                ${idx + 1}
                            </span>
                            <span class="text-xs text-slate-400 font-semibold">【${q.chapter} · ${typeLabel}】</span>
                        </div>
                    </div>

                    <h3 class="text-base sm:text-lg font-bold text-white leading-relaxed">
                        ${q.title}
                    </h3>

                    <!-- Options -->
                    <div class="space-y-2.5 pt-2">
                        ${q.options.map(opt => `
                            <div data-qid="${q.id}" data-type="${q.type}" data-key="${opt.key}" class="quiz-option p-4 rounded-2xl bg-slate-950 border border-slate-800/80 cursor-pointer flex items-center gap-3 text-sm text-slate-200">
                                <span class="w-6 h-6 rounded-lg bg-slate-800 text-slate-300 font-bold font-mono text-xs flex items-center justify-center border border-slate-700 option-badge">
                                    ${opt.key}
                                </span>
                                <span>${opt.text}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }).join('');

        document.querySelectorAll('.quiz-option').forEach(optionEl => {
            optionEl.addEventListener('click', () => {
                const qid = optionEl.getAttribute('data-qid');
                const qtype = optionEl.getAttribute('data-type');
                const key = optionEl.getAttribute('data-key');

                if (qtype === 'single') {
                    // Single choice: exclusive select
                    userAnswers[qid] = key;

                    const siblingOptions = document.querySelectorAll(`.quiz-option[data-qid="${qid}"]`);
                    siblingOptions.forEach(opt => {
                        opt.classList.remove('selected');
                        opt.querySelector('.option-badge').classList.remove('bg-sky-500', 'text-white', 'border-sky-400');
                    });

                    optionEl.classList.add('selected');
                    optionEl.querySelector('.option-badge').classList.add('bg-sky-500', 'text-white', 'border-sky-400');

                } else {
                    // Multiple choice: toggle selection
                    let currentAns = userAnswers[qid] ? userAnswers[qid].split('') : [];
                    if (currentAns.includes(key)) {
                        currentAns = currentAns.filter(k => k !== key);
                        optionEl.classList.remove('selected');
                        optionEl.querySelector('.option-badge').classList.remove('bg-indigo-500', 'text-white', 'border-indigo-400');
                    } else {
                        currentAns.push(key);
                        currentAns.sort();
                        optionEl.classList.add('selected');
                        optionEl.querySelector('.option-badge').classList.add('bg-indigo-500', 'text-white', 'border-indigo-400');
                    }

                    if (currentAns.length > 0) {
                        userAnswers[qid] = currentAns.join('');
                    } else {
                        delete userAnswers[qid];
                    }
                }

                const answeredCount = Object.keys(userAnswers).length;
                examProgressText.textContent = `${answeredCount} / ${questionBank.length}`;
            });
        });

        examProgressText.textContent = `0 / ${questionBank.length}`;
    };

    // --- Timer Logic (75 mins = 4500 secs) ---
    const startTimer = () => {
        if (timerInterval) clearInterval(timerInterval);
        updateTimerDisplay();

        timerInterval = setInterval(() => {
            timeRemaining--;
            timeElapsed++;
            updateTimerDisplay();

            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                alert('考试时间到（75分钟），系统已为您自动交卷！');
                submitExam();
            }
        }, 1000);
    };

    const updateTimerDisplay = () => {
        const mins = Math.floor(timeRemaining / 60);
        const secs = timeRemaining % 60;
        examTimer.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    };

    // Exit Exam Handlers
    const exitExamHandler = () => {
        if (confirm('确定要退出本次随堂考试吗？未交卷的选项将被清空。')) {
            if (timerInterval) clearInterval(timerInterval);
            window.location.reload();
        }
    };
    if (btnExitExamHeader) btnExitExamHeader.addEventListener('click', exitExamHandler);
    if (btnExitExamFooter) btnExitExamFooter.addEventListener('click', exitExamHandler);

    // --- Submit Exam Scoring Engine (40 single @ 1.5 + 20 multi @ 2.0 = 100 pts) ---
    btnSubmitExam.addEventListener('click', () => {
        const answeredCount = Object.keys(userAnswers).length;
        if (answeredCount < questionBank.length) {
            if (!confirm(`您还有 ${questionBank.length - answeredCount} 道题未作答，确定要现在交卷吗？`)) {
                return;
            }
        }
        submitExam();
    });

    const submitExam = () => {
        if (timerInterval) clearInterval(timerInterval);

        let totalScore = 0;
        let correctCount = 0;

        questionBank.forEach(q => {
            const userAns = userAnswers[q.id] || '';
            const correctAns = q.answer;

            if (q.type === 'single') {
                if (userAns === correctAns) {
                    totalScore += 1.5;
                    correctCount++;
                }
            } else {
                // Multiple choice: exact match
                if (userAns.split('').sort().join('') === correctAns.split('').sort().join('')) {
                    totalScore += 2.0;
                    correctCount++;
                }
            }
        });

        // Round score to 1 decimal place if needed
        totalScore = Math.round(totalScore * 10) / 10;
        const accuracy = Math.round((correctCount / questionBank.length) * 100);
        const durationMin = Math.floor(timeElapsed / 60);
        const durationSec = timeElapsed % 60;
        const durationStr = `${String(durationMin).padStart(2, '0')}:${String(durationSec).padStart(2, '0')}`;

        const newRecord = {
            id: currentStudent.id,
            name: currentStudent.name,
            score: totalScore,
            accuracy: `${accuracy}%`,
            duration: durationStr,
            userAnswers: { ...userAnswers },
            scoreCheckedCount: 0,
            timestamp: new Date().toLocaleString('zh-CN', { hour12: false })
        };

        saveSubmissionRecord(newRecord);
        renderReadOnlyScoreResult(newRecord, 0);
    };

    // --- Render Read-Only Score Result Page ---
    const renderReadOnlyScoreResult = (record, checkCount) => {
        viewLogin.classList.add('hidden');
        viewExam.classList.add('hidden');
        viewResult.classList.remove('hidden');

        resultStudentInfo.textContent = `${record.id} - ${record.name}`;
        
        const displayScoreText = `${record.score} <span class="text-base font-normal text-slate-400">/ 100分</span>`;
        resultScore.innerHTML = displayScoreText;
        if (resultScoreTop) resultScoreTop.innerHTML = displayScoreText;

        resultAccuracy.textContent = record.accuracy;
        resultDuration.textContent = record.duration;

        if (checkCount > 0) {
            readOnlyQueryAlert.classList.remove('hidden');
            let secLeft = 15;
            readOnlyCountdown.textContent = secLeft;

            const readOnlyTimer = setInterval(() => {
                secLeft--;
                readOnlyCountdown.textContent = secLeft;
                if (secLeft <= 0) {
                    clearInterval(readOnlyTimer);
                    try { window.close(); } catch (e) {}
                    window.location.reload();
                }
            }, 1000);
        }

        // Render Breakdown
        resultBreakdown.innerHTML = questionBank.map((q, idx) => {
            const userAns = (record.userAnswers && record.userAnswers[q.id]) || '未作答';
            const correctAns = q.answer;
            
            let isCorrect = false;
            if (q.type === 'single') {
                isCorrect = userAns === correctAns;
            } else {
                isCorrect = userAns.split('').sort().join('') === correctAns.split('').sort().join('');
            }

            const isMulti = q.type === 'multiple';
            const typeLabel = isMulti ? '多选题 · 2分' : '单选题 · 1.5分';

            return `
                <div class="question-card bg-slate-900 border ${isCorrect ? 'border-emerald-500/40' : 'border-rose-500/40'} rounded-3xl p-6 space-y-4">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <span class="w-7 h-7 rounded-xl ${isCorrect ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border-rose-500/30'} border flex items-center justify-center font-bold font-mono text-xs">
                                ${idx + 1}
                            </span>
                            <span class="text-xs text-slate-400">【${q.chapter} · ${typeLabel}】</span>
                        </div>

                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-1 rounded-xl text-xs font-bold font-mono ${isCorrect ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'}">
                                ${isCorrect ? '✓ 正确 (' + (isMulti ? '2分' : '1.5分') + ')' : '✗ 错误 (0分)'}
                            </span>
                        </div>
                    </div>

                    <h4 class="text-sm font-bold text-white leading-relaxed">${q.title}</h4>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono pt-1">
                        <div class="p-3 rounded-xl ${isCorrect ? 'bg-emerald-950/40 border border-emerald-800/60 text-emerald-300' : 'bg-rose-950/40 border border-rose-800/60 text-rose-300'}">
                            您的选择：<strong class="text-sm">${userAns}</strong>
                        </div>
                        <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 text-sky-300">
                            标准答案：<strong class="text-sm text-sky-400">${correctAns}</strong>
                        </div>
                    </div>

                    <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 text-xs text-slate-300 leading-relaxed">
                        <strong class="text-sky-400 block mb-1">权威解析：</strong>
                        ${q.explanation}
                    </div>
                </div>
            `;
        }).join('');
    };

    btnRestartStudent.addEventListener('click', () => {
        window.location.reload();
    });

});
"""

app_js_code = app_js_template.replace("REPLACE_QUESTIONS_JSON", questions_json)

with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\app.js', 'w', encoding='utf-8') as f:
    f.write(app_js_code)

print("Updated online-exam-system/app.js with 60 questions and single/multiple scoring logic successfully!")
