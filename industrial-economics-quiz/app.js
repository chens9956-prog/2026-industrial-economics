// Main Application Logic for Industrial Economics Quiz Bank

document.addEventListener('DOMContentLoaded', () => {
    // --- State Management ---
    let currentType = 'all';
    let searchQuery = '';
    let isQuizMode = false;
    let userAnswers = {}; // { questionId: selectedOptionIndex }

    // --- DOM Elements ---
    const questionsContainer = document.getElementById('questions-container');
    const emptyState = document.getElementById('empty-state');
    const searchInput = document.getElementById('search-input');
    const btnClearSearch = document.getElementById('btn-clear-search');
    const typeTabs = document.querySelectorAll('.type-tab');
    const modeBrowse = document.getElementById('mode-browse');
    const modeQuiz = document.getElementById('mode-quiz');
    const quizBanner = document.getElementById('quiz-banner');
    const quizProgress = document.getElementById('quiz-progress');
    const quizAccuracy = document.getElementById('quiz-accuracy');
    const btnResetQuiz = document.getElementById('btn-reset-quiz');
    const btnTheme = document.getElementById('btn-theme');
    const btnExport = document.getElementById('btn-export');
    const exportModal = document.getElementById('export-modal');
    const closeModal = document.getElementById('close-modal');
    const exportMarkdown = document.getElementById('export-markdown');
    const exportPrint = document.getElementById('export-print');

    // --- Stats Counters ---
    const statTotal = document.getElementById('stat-total');
    const statCalc = document.getElementById('stat-calc');
    const countAll = document.getElementById('count-all');
    const countChoice = document.getElementById('count-choice');
    const countTerm = document.getElementById('count-term');
    const countShort = document.getElementById('count-short');
    const countCalc = document.getElementById('count-calc');
    const countEssay = document.getElementById('count-essay');

    // --- Initialize Theme ---
    const initTheme = () => {
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    };
    initTheme();

    btnTheme.addEventListener('click', () => {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.theme = 'light';
        } else {
            document.documentElement.classList.add('dark');
            localStorage.theme = 'dark';
        }
    });

    // --- Initialize Counts & Stats ---
    const updateStats = () => {
        statTotal.textContent = questionsData.length;
        const calcCount = questionsData.filter(q => q.type === 'calc').length;
        statCalc.textContent = calcCount;

        countAll.textContent = questionsData.length;
        countChoice.textContent = questionsData.filter(q => q.type === 'choice').length;
        countTerm.textContent = questionsData.filter(q => q.type === 'term').length;
        countShort.textContent = questionsData.filter(q => q.type === 'short').length;
        countCalc.textContent = calcCount;
        countEssay.textContent = questionsData.filter(q => q.type === 'essay').length;
    };
    updateStats();

    // --- Render Questions ---
    const renderQuestions = () => {
        // Filter logic
        const filtered = questionsData.filter(q => {
            const matchesType = currentType === 'all' || q.type === currentType;
            const matchesSearch = !searchQuery || 
                q.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
                q.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
                (q.answer && String(q.answer).toLowerCase().includes(searchQuery.toLowerCase()));
            return matchesType && matchesSearch;
        });

        if (filtered.length === 0) {
            questionsContainer.innerHTML = '';
            emptyState.classList.remove('hidden');
            return;
        }

        emptyState.classList.add('hidden');

        questionsContainer.innerHTML = filtered.map((q, index) => {
            return createQuestionCardHTML(q, index + 1);
        }).join('');

        // Trigger KaTeX Math rendering on newly inserted elements
        if (window.renderMathInElement) {
            renderMathInElement(questionsContainer, {
                delimiters: [
                    {left: '$$', right: '$$', display: true},
                    {left: '$', right: '$', display: false},
                    {left: '\\(', right: '\\)', display: false},
                    {left: '\\[', right: '\\]', display: true}
                ],
                throwOnError: false
            });
        }

        // Attach Card Event Listeners
        attachCardListeners();
    };

    // --- Question Card HTML Generator ---
    const createQuestionCardHTML = (q, num) => {
        const typeBadgeMap = {
            choice: { text: '单项选择题', color: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-300' },
            term: { text: '名词解释', color: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300' },
            short: { text: '简答题', color: 'bg-amber-100 text-amber-700 dark:bg-amber-900/50 dark:text-amber-300' },
            calc: { text: '计算推导题', color: 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900/50 dark:text-cyan-300' },
            essay: { text: '综述/论述题', color: 'bg-purple-100 text-purple-700 dark:bg-purple-900/50 dark:text-purple-300' }
        };

        const badge = typeBadgeMap[q.type] || { text: '试题', color: 'bg-slate-100 text-slate-700' };
        const userChoice = userAnswers[q.id];

        let optionsHTML = '';
        if (q.type === 'choice' && q.options) {
            optionsHTML = `<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-4">` +
                q.options.map((opt, idx) => {
                    let btnStyle = "bg-slate-50 dark:bg-slate-800/80 border-slate-200 dark:border-slate-700/80 text-slate-700 dark:text-slate-200 hover:border-indigo-400 hover:bg-indigo-50/50 dark:hover:bg-slate-800";
                    
                    if (userChoice !== undefined) {
                        if (idx === q.answer) {
                            btnStyle = "bg-emerald-50 dark:bg-emerald-950/60 border-emerald-500 text-emerald-700 dark:text-emerald-300 font-semibold ring-2 ring-emerald-500/20";
                        } else if (idx === userChoice && userChoice !== q.answer) {
                            btnStyle = "bg-rose-50 dark:bg-rose-950/60 border-rose-500 text-rose-700 dark:text-rose-300 font-semibold ring-2 ring-rose-500/20";
                        }
                    }

                    return `
                        <button data-qid="${q.id}" data-optidx="${idx}" class="option-btn text-left p-3.5 rounded-xl border text-sm transition-all flex items-center justify-between ${btnStyle}">
                            <span>${opt}</span>
                            ${userChoice !== undefined ? (
                                idx === q.answer ? '<i class="fa-solid fa-circle-check text-emerald-500"></i>' : 
                                (idx === userChoice ? '<i class="fa-solid fa-circle-xmark text-rose-500"></i>' : '')
                            ) : ''}
                        </button>
                    `;
                }).join('') +
            `</div>`;
        }

        let answerContent = '';
        if (q.type === 'choice') {
            answerContent = `<div class="font-bold text-emerald-600 dark:text-emerald-400 mb-2">正确答案：${q.options[q.answer]}</div>
                             <div class="text-slate-600 dark:text-slate-300 text-sm whitespace-pre-line">${q.explanation}</div>`;
        } else {
            answerContent = `<div class="text-slate-700 dark:text-slate-200 text-sm leading-relaxed whitespace-pre-line">${q.answer}</div>`;
        }

        const isAnswerShown = isQuizMode && (q.type !== 'choice' || userChoice !== undefined);

        return `
            <div class="question-card p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800/80 shadow-sm relative overflow-hidden">
                <!-- Card Header -->
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <div class="flex items-center gap-2">
                        <span class="text-xs px-3 py-1 rounded-lg font-bold ${badge.color}">${badge.text}</span>
                        <span class="text-xs px-2.5 py-1 rounded-lg font-medium bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400">
                            <i class="fa-solid fa-tag mr-1 text-slate-400"></i>${q.category}
                        </span>
                    </div>
                    <div class="flex items-center gap-3">
                        <span class="text-xs text-slate-400 font-medium">难度: ${q.difficulty}</span>
                        <button data-qid="${q.id}" class="btn-copy-q text-slate-400 hover:text-indigo-500 text-xs transition-colors" title="复制题目">
                            <i class="fa-regular fa-copy"></i>
                        </button>
                    </div>
                </div>

                <!-- Question Text -->
                <div class="text-base sm:text-lg font-bold text-slate-800 dark:text-slate-100 my-2 leading-relaxed">
                    <span class="text-indigo-600 dark:text-indigo-400 mr-1.5">${num}.</span> ${q.question}
                </div>

                <!-- Options (if choice) -->
                ${optionsHTML}

                <!-- Answer Toggle & Answer Box -->
                <div class="mt-5 pt-4 border-t border-slate-100 dark:border-slate-800/60">
                    <button data-target="ans-${q.id}" class="btn-toggle-ans w-full flex items-center justify-between text-xs font-bold text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 py-1 transition-colors">
                        <span><i class="fa-solid fa-lightbulb mr-1.5 text-amber-500"></i>${isAnswerShown ? '隐藏标准解析与推导过程' : '查看标准解析与推导过程'}</span>
                        <i class="fa-solid ${isAnswerShown ? 'fa-chevron-up' : 'fa-chevron-down'} transition-transform"></i>
                    </button>

                    <div id="ans-${q.id}" class="answer-box mt-3 p-4 rounded-2xl bg-indigo-50/60 dark:bg-slate-800/60 border border-indigo-100 dark:border-slate-700/60 transition-all ${isAnswerShown ? '' : 'hidden'}">
                        ${answerContent}
                    </div>
                </div>
            </div>
        `;
    };

    // --- Card Event Listeners ---
    const attachCardListeners = () => {
        // Toggle Answer Buttons
        document.querySelectorAll('.btn-toggle-ans').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const targetId = btn.getAttribute('data-target');
                const ansBox = document.getElementById(targetId);
                const isHidden = ansBox.classList.contains('hidden');
                
                if (isHidden) {
                    ansBox.classList.remove('hidden');
                    btn.querySelector('span').innerHTML = '<i class="fa-solid fa-lightbulb mr-1.5 text-amber-500"></i>隐藏标准解析与推导过程';
                    btn.querySelector('.fa-solid:last-child').className = 'fa-solid fa-chevron-up transition-transform';
                } else {
                    ansBox.classList.add('hidden');
                    btn.querySelector('span').innerHTML = '<i class="fa-solid fa-lightbulb mr-1.5 text-amber-500"></i>查看标准解析与推导过程';
                    btn.querySelector('.fa-solid:last-child').className = 'fa-solid fa-chevron-down transition-transform';
                }
            });
        });

        // Option Click Handlers (Quiz Mode)
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const qid = btn.getAttribute('data-qid');
                const optidx = parseInt(btn.getAttribute('data-optidx'));
                
                userAnswers[qid] = optidx;
                updateQuizScore();
                renderQuestions();
            });
        });

        // Copy Question Button
        document.querySelectorAll('.btn-copy-q').forEach(btn => {
            btn.addEventListener('click', () => {
                const qid = btn.getAttribute('data-qid');
                const qObj = questionsData.find(item => item.id === qid);
                if (qObj) {
                    let text = `【产业经济学试题】\n题目：${qObj.question}\n`;
                    if (qObj.options) {
                        text += qObj.options.join('\n') + '\n';
                    }
                    text += `标准答案与解析：\n${qObj.type === 'choice' ? qObj.options[qObj.answer] + '\n' + qObj.explanation : qObj.answer}`;
                    
                    navigator.clipboard.writeText(text).then(() => {
                        btn.innerHTML = '<i class="fa-solid fa-check text-emerald-500"></i>';
                        setTimeout(() => {
                            btn.innerHTML = '<i class="fa-regular fa-copy"></i>';
                        }, 1500);
                    });
                }
            });
        });
    };

    // --- Quiz Score Calculation ---
    const updateQuizScore = () => {
        const choiceQuestions = questionsData.filter(q => q.type === 'choice');
        const answeredQids = Object.keys(userAnswers);
        
        let correctCount = 0;
        answeredQids.forEach(qid => {
            const q = questionsData.find(item => item.id === qid);
            if (q && q.type === 'choice' && userAnswers[qid] === q.answer) {
                correctCount++;
            }
        });

        quizProgress.textContent = `${answeredQids.length} / ${choiceQuestions.length}`;
        const accuracy = answeredQids.length > 0 ? Math.round((correctCount / answeredQids.length) * 100) : 100;
        quizAccuracy.textContent = `${accuracy}%`;
    };

    // --- Event Handlers ---
    
    // Type Tabs Filter
    typeTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            typeTabs.forEach(t => {
                t.classList.remove('active-tab', 'bg-indigo-600', 'text-white');
                t.classList.add('bg-white', 'dark:bg-slate-900', 'text-slate-600', 'dark:text-slate-300');
            });

            tab.classList.add('active-tab', 'bg-indigo-600', 'text-white');
            tab.classList.remove('bg-white', 'dark:bg-slate-900', 'text-slate-600', 'dark:text-slate-300');

            currentType = tab.getAttribute('data-type');
            renderQuestions();
        });
    });

    // Search Input
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.trim();
        if (searchQuery) {
            btnClearSearch.classList.remove('hidden');
        } else {
            btnClearSearch.classList.add('hidden');
        }
        renderQuestions();
    });

    btnClearSearch.addEventListener('click', () => {
        searchInput.value = '';
        searchQuery = '';
        btnClearSearch.classList.add('hidden');
        renderQuestions();
    });

    // Mode Toggle
    modeBrowse.addEventListener('click', () => {
        isQuizMode = false;
        modeBrowse.classList.add('bg-white', 'dark:bg-slate-700', 'text-indigo-600', 'dark:text-indigo-300', 'shadow-sm');
        modeBrowse.classList.remove('text-slate-600', 'dark:text-slate-400');
        
        modeQuiz.classList.remove('bg-white', 'dark:bg-slate-700', 'text-indigo-600', 'dark:text-indigo-300', 'shadow-sm');
        modeQuiz.classList.add('text-slate-600', 'dark:text-slate-400');
        
        quizBanner.classList.add('hidden');
        renderQuestions();
    });

    modeQuiz.addEventListener('click', () => {
        isQuizMode = true;
        modeQuiz.classList.add('bg-white', 'dark:bg-slate-700', 'text-indigo-600', 'dark:text-indigo-300', 'shadow-sm');
        modeQuiz.classList.remove('text-slate-600', 'dark:text-slate-400');
        
        modeBrowse.classList.remove('bg-white', 'dark:bg-slate-700', 'text-indigo-600', 'dark:text-indigo-300', 'shadow-sm');
        modeBrowse.classList.add('text-slate-600', 'dark:text-slate-400');
        
        quizBanner.classList.remove('hidden');
        updateQuizScore();
        renderQuestions();
    });

    btnResetQuiz.addEventListener('click', () => {
        userAnswers = {};
        updateQuizScore();
        renderQuestions();
    });

    // Export Modal Controls
    btnExport.addEventListener('click', () => {
        exportModal.classList.remove('hidden');
    });

    closeModal.addEventListener('click', () => {
        exportModal.classList.add('hidden');
    });

    exportModal.addEventListener('click', (e) => {
        if (e.target === exportModal) {
            exportModal.classList.add('hidden');
        }
    });

    // Export Markdown
    exportMarkdown.addEventListener('click', () => {
        let mdContent = `# 产业经济学精选题库与试卷\n\n导出时间：${new Date().toLocaleDateString()}\n\n---\n\n`;
        
        questionsData.forEach((q, idx) => {
            mdContent += `### ${idx + 1}. [${q.category}] ${q.question}\n\n`;
            if (q.type === 'choice' && q.options) {
                q.options.forEach(opt => {
                    mdContent += `- ${opt}\n`;
                });
                mdContent += `\n**正确答案**：${q.options[q.answer]}\n\n**解析**：${q.explanation}\n\n`;
            } else {
                mdContent += `**参考答案与推导过程**：\n\n${q.answer}\n\n`;
            }
            mdContent += `---\n\n`;
        });

        const blob = new Blob([mdContent], { type: 'text/markdown;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `产业经济学试题库_${new Date().toISOString().slice(0, 10)}.md`;
        link.click();
        
        exportModal.classList.add('hidden');
    });

    // Export Print / PDF
    exportPrint.addEventListener('click', () => {
        exportModal.classList.add('hidden');
        window.print();
    });

    // --- Initial Render ---
    renderQuestions();
});
