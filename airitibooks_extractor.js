// 華藝電子書 (AiritiBooks / iRead eBooks) 全自動高畫質書籍提取引擎 v1.0
// 使用方法：在 AiritiBooks 閱讀頁面打開 F12 -> Console -> 貼上本代碼並按 Enter

(function initAiritiBooksExtractor() {
    console.log("🚀 正在啟動 華藝電子書 (AiritiBooks) 全自動提取器...");

    if (window._airitiExtractorRunning) {
        alert("⚠️ 提取器已在運行中！");
        return;
    }
    window._airitiExtractorRunning = true;

    let bookTitle = document.title.split('-')[0].split('|')[0].trim() || "華藝電子書";
    bookTitle = bookTitle.replace(/[\\/:*?"<>|]/g, "_");

    let extractedPages = [];
    let seenFingerprints = new Set();
    let isExtracting = false;
    let flipTimer = null;
    let flipIntervalMs = 2000;

    // 建立浮動控制面板 (HUD)
    const hud = document.createElement("div");
    hud.id = "airiti-hud";
    hud.style.cssText = `
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 9999999;
        background: rgba(15, 23, 42, 0.95);
        color: #fff;
        padding: 18px 22px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        border: 1px solid rgba(255,255,255,0.15);
        min-width: 280px;
        backdrop-filter: blur(8px);
    `;

    hud.innerHTML = `
        <div style="font-weight: 700; font-size: 15px; margin-bottom: 8px; color: #38bdf8; display: flex; justify-content: space-between; align-items: center;">
            <span>📚 華藝電子書全書提取器</span>
            <span style="font-size: 11px; background: #0284c7; padding: 2px 6px; border-radius: 4px;">v1.0</span>
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-bottom: 12px; max-width: 260px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            書名: <strong style="color: #f1f5f9;">${bookTitle}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 12px; background: rgba(255,255,255,0.05); padding: 8px 12px; border-radius: 6px;">
            <span style="font-size: 13px; color: #cbd5e1;">已抓取頁數:</span>
            <span id="airiti-page-count" style="font-size: 16px; font-weight: bold; color: #4ade80;">0 頁</span>
        </div>
        <div style="display: flex; gap: 8px; margin-bottom: 10px;">
            <button id="airiti-btn-start" style="flex: 1; padding: 8px 12px; background: #0284c7; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px;">
                ▶ 開始自動翻頁抓取
            </button>
            <button id="airiti-btn-download" style="flex: 1; padding: 8px 12px; background: #16a34a; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px;">
                📦 下載 JSON 數據包
            </button>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #64748b;">
            <span>翻頁間隔: 2.0秒</span>
            <span id="airiti-btn-reset" style="color: #ef4444; cursor: pointer; text-decoration: underline;">重置清空</span>
        </div>
    `;

    document.body.appendChild(hud);

    function captureCurrentPage() {
        // 抓取當前視窗中的 canvas 或 高清 img
        const canvases = document.querySelectorAll("canvas");
        let bestCanvas = null;
        let maxArea = 0;

        canvases.forEach(c => {
            const area = c.width * c.height;
            if (area > maxArea && c.width > 300 && c.height > 300) {
                maxArea = area;
                bestCanvas = c;
            }
        });

        if (bestCanvas) {
            try {
                const dataUrl = bestCanvas.toDataURL("image/jpeg", 0.95);
                const fp = dataUrl.slice(30, 90);
                if (!seenFingerprints.has(fp)) {
                    seenFingerprints.add(fp);
                    extractedPages.push(dataUrl);
                    document.getElementById("airiti-page-count").innerText = `${extractedPages.length} 頁`;
                    console.log(`[AiritiBooks] 成功捕獲第 ${extractedPages.length} 頁 (解析度: ${bestCanvas.width}x${bestCanvas.height})`);
                }
            } catch (e) {
                console.warn("[AiritiBooks] Canvas 導出異常:", e);
            }
        }
    }

    function triggerNextPage() {
        captureCurrentPage();
        
        // 觸發 AiritiBooks 下一頁按鈕
        const nextBtn = document.getElementById("next_page") || 
                        document.querySelector(".btn_next") || 
                        document.querySelector("[title*='下一頁']") ||
                        document.querySelector("[class*='next']");

        if (nextBtn) {
            nextBtn.click();
        } else {
            // 嘗試按右方向鍵
            document.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', keyCode: 39, bubbles: true }));
        }
    }

    // 事件監聽
    document.getElementById("airiti-btn-start").onclick = function() {
        if (!isExtracting) {
            isExtracting = true;
            this.innerText = "⏸ 暫停抓取";
            this.style.background = "#d97706";
            captureCurrentPage();
            flipTimer = setInterval(triggerNextPage, flipIntervalMs);
        } else {
            isExtracting = false;
            this.innerText = "▶ 繼續自動抓取";
            this.style.background = "#0284c7";
            clearInterval(flipTimer);
        }
    };

    document.getElementById("airiti-btn-download").onclick = function() {
        if (extractedPages.length === 0) {
            alert("⚠️ 尚未抓取到任何頁面數據！請先點擊「開始自動翻頁抓取」。");
            return;
        }
        
        if (isExtracting) {
            document.getElementById("airiti-btn-start").click();
        }

        const blob = new Blob([JSON.stringify(extractedPages)], { type: "application/json" });
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = `${bookTitle}_全部${extractedPages.length}頁數據.json`;
        a.click();
        console.log(`🎉 數據包已下載: ${a.download}`);
    };

    document.getElementById("airiti-btn-reset").onclick = function() {
        if (confirm("確定要清空已抓取的頁面數據嗎？")) {
            if (isExtracting) {
                document.getElementById("airiti-btn-start").click();
            }
            extractedPages = [];
            seenFingerprints.clear();
            document.getElementById("airiti-page-count").innerText = "0 頁";
        }
    };

    console.log("✅ 華藝電子書提取控制台已就緒！");
})();
