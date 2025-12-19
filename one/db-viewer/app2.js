// 状态管理
let currentTable = null;
let currentData = null;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    loadTables();
    document.getElementById('queryBtn').addEventListener('click', queryData);
    document.getElementById('tableSelect').addEventListener('change', (e) => {
        currentTable = e.target.value;
    });
});

// 加载表列表
async function loadTables() {
    try {
        showStatus('正在加载表列表...', 'info');
        
        const response = await fetch('http://localhost:8888/api/tables');
        const data = await response.json();
        
        if (data.success) {
            const select = document.getElementById('tableSelect');
            select.innerHTML = '';
            
            data.tables.forEach((table, index) => {
                const option = document.createElement('option');
                option.value = table;
                option.textContent = table;
                if (index === 0) option.selected = true;
                select.appendChild(option);
            });
            
            currentTable = data.tables[0];
            showStatus(`成功加载 ${data.tables.length} 个表`, 'success');
        } else {
            showStatus(`加载失败: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`连接错误: ${error.message}。请确保本地服务器运行中`, 'error');
        console.error('Error:', error);
    }
}

// 查询数据
async function queryData() {
    if (!currentTable) {
        showStatus('请先选择一个表', 'error');
        return;
    }
    
    const limit = parseInt(document.getElementById('limitInput').value) || 1000;
    
    if (limit < 1 || limit > 10000) {
        showStatus('行数必须在 1-10000 之间', 'error');
        return;
    }
    
    try {
        const btn = document.getElementById('queryBtn');
        btn.disabled = true;
        btn.innerHTML = '<span class="loading"></span> 查询中...';
        
        showStatus('正在查询数据...', 'info');
        
        const startTime = performance.now();
        const response = await fetch('http://localhost:8888/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                table: currentTable,
                limit: limit
            })
        });
        const endTime = performance.now();
        
        const data = await response.json();
        
        if (data.success) {
            currentData = data.data;
            renderTable(data.columns, data.data);
            showStats(data.data.length, data.columns.length, Math.round(endTime - startTime));
            showStatus(`成功查询 ${data.data.length} 条数据`, 'success');
        } else {
            showStatus(`查询失败: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`查询错误: ${error.message}`, 'error');
        console.error('Error:', error);
    } finally {
        const btn = document.getElementById('queryBtn');
        btn.disabled = false;
        btn.innerHTML = '<span>🔍 查询数据</span>';
    }
}

// 渲染表格
function renderTable(columns, rows) {
    // 渲染表头
    const headerRow = document.getElementById('headerRow');
    headerRow.innerHTML = columns.map(col => `<th>${escapeHtml(col)}</th>`).join('');
    
    // 渲染数据行
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = rows.map((row, rowIndex) => {
        const cells = columns.map(col => {
            let value = row[col];
            
            // 处理不同类型的值
            if (value === null || value === undefined) {
                return '<td class="text-gray-400">NULL</td>';
            }
            
            if (typeof value === 'object') {
                value = JSON.stringify(value);
            }
            
            const displayValue = String(value).substring(0, 200);
            const isLong = String(value).length > 200;
            
            return `<td title="${isLong ? escapeHtml(String(value)) : ''}">${escapeHtml(displayValue)}${isLong ? '...' : ''}</td>`;
        }).join('');
        
        return `<tr class="table-row">${cells}</tr>`;
    }).join('');
    
    // 显示统计信息
    document.getElementById('statsContainer').classList.remove('hidden');
}

// 显示统计信息
function showStats(rowCount, colCount, queryTime) {
    document.getElementById('rowCount').textContent = rowCount.toLocaleString();
    document.getElementById('colCount').textContent = colCount;
    document.getElementById('queryTime').textContent = `${queryTime}ms`;
}

// 显示状态信息
function showStatus(message, type = 'info') {
    const container = document.getElementById('statusContainer');
    
    let className = 'success-message';
    let icon = '✓';
    
    if (type === 'error') {
        className = 'error-message';
        icon = '✗';
    } else if (type === 'info') {
        className = 'bg-blue-50 border-l-4 border-blue-400 text-blue-700 p-3 rounded';
        icon = 'ℹ';
    }
    
    container.innerHTML = `<div class="${className}">${icon} ${message}</div>`;
    container.classList.remove('hidden');
    
    // 3秒后自动隐藏
    setTimeout(() => {
        container.classList.add('hidden');
    }, 3000);
}

// HTML转义
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
