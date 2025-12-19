// 数据库查看工具 - 前端 JavaScript
// 修复版本：确保正确显示所有数据

let currentTable = '';
let currentLimit = 1000;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成，开始初始化...');
    
    // 加载表列表
    loadTables();
    
    // 绑定查询按钮事件
    document.getElementById('queryBtn').addEventListener('click', function() {
        queryData();
    });
    
    // 绑定回车键查询
    document.getElementById('limitInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            queryData();
        }
    });
});

/**
 * 加载所有表列表
 */
async function loadTables() {
    try {
        const response = await fetch('/api/tables');
        const result = await response.json();
        
        if (result.success) {
            const select = document.getElementById('tableSelect');
            select.innerHTML = '<option value="">请选择表...</option>';
            
            result.tables.forEach(table => {
                const option = document.createElement('option');
                option.value = table;
                option.textContent = table;
                select.appendChild(option);
            });
            
            console.log(`✓ 加载了 ${result.tables.length} 个表`);
        } else {
            showStatus('error', '加载表列表失败: ' + result.error);
        }
    } catch (error) {
        console.error('加载表列表失败:', error);
        showStatus('error', '加载表列表失败: ' + error.message);
    }
}

/**
 * 查询表数据
 */
async function queryData() {
    const tableSelect = document.getElementById('tableSelect');
    const limitInput = document.getElementById('limitInput');
    const queryBtn = document.getElementById('queryBtn');
    
    const table = tableSelect.value;
    const limit = parseInt(limitInput.value) || 1000;
    
    // 验证输入
    if (!table) {
        showStatus('error', '请先选择数据表');
        return;
    }
    
    if (limit < 1 || limit > 10000) {
        showStatus('error', '查询行数必须在 1-10000 之间');
        return;
    }
    
    // 保存当前状态
    currentTable = table;
    currentLimit = limit;
    
    // 显示加载状态
    queryBtn.disabled = true;
    queryBtn.innerHTML = '<span class="loading"></span> 查询中...';
    
    const startTime = Date.now();
    
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                table: table,
                limit: limit
            })
        });
        
        const result = await response.json();
        const queryTime = Date.now() - startTime;
        
        if (result.success) {
            // 显示数据
            displayData(result.columns, result.data, result.returned, queryTime);
            showStatus('success', `查询成功！返回 ${result.returned} 行数据，耗时 ${queryTime}ms`);
        } else {
            showStatus('error', '查询失败: ' + result.error);
            clearTable();
        }
    } catch (error) {
        console.error('查询失败:', error);
        showStatus('error', '查询失败: ' + error.message);
        clearTable();
    } finally {
        queryBtn.disabled = false;
        queryBtn.innerHTML = '🔍 查询数据';
    }
}

/**
 * 显示数据表格
 */
function displayData(columns, data, returned, queryTime) {
    const headerRow = document.getElementById('headerRow');
    const tableBody = document.getElementById('tableBody');
    const statsContainer = document.getElementById('statsContainer');
    const rowCountEl = document.getElementById('rowCount');
    const colCountEl = document.getElementById('colCount');
    const queryTimeEl = document.getElementById('queryTime');
    
    // 清空表格
    headerRow.innerHTML = '';
    tableBody.innerHTML = '';
    
    if (!columns || columns.length === 0) {
        tableBody.innerHTML = '<tr><td class="p-8 text-center text-gray-500">表没有列</td></tr>';
        return;
    }
    
    if (!data || data.length === 0) {
        tableBody.innerHTML = '<tr><td class="p-8 text-center text-gray-500">表中没有数据</td></tr>';
        // 显示表头
        columns.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            headerRow.appendChild(th);
        });
        // 显示统计
        statsContainer.classList.remove('hidden');
        rowCountEl.textContent = '0';
        colCountEl.textContent = columns.length;
        queryTimeEl.textContent = queryTime + 'ms';
        return;
    }
    
    // 创建表头
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        th.title = col; // 鼠标悬停显示完整列名
        headerRow.appendChild(th);
    });
    
    // 创建数据行
    data.forEach((row, rowIndex) => {
        const tr = document.createElement('tr');
        tr.className = 'table-row';
        
        columns.forEach(col => {
            const td = document.createElement('td');
            let value = row[col];
            
            // 处理不同类型的值
            if (value === null || value === undefined) {
                td.textContent = '';
                td.style.color = '#999';
            } else if (typeof value === 'object') {
                td.textContent = JSON.stringify(value);
            } else {
                td.textContent = String(value);
            }
            
            // 添加标题（鼠标悬停显示完整内容）
            td.title = td.textContent;
            
            tr.appendChild(td);
        });
        
        tableBody.appendChild(tr);
    });
    
    // 显示统计信息
    statsContainer.classList.remove('hidden');
    rowCountEl.textContent = returned.toLocaleString();
    colCountEl.textContent = columns.length;
    queryTimeEl.textContent = queryTime + 'ms';
    
    console.log(`✓ 显示数据: ${returned} 行, ${columns.length} 列, 耗时 ${queryTime}ms`);
}

/**
 * 清空表格
 */
function clearTable() {
    const headerRow = document.getElementById('headerRow');
    const tableBody = document.getElementById('tableBody');
    const statsContainer = document.getElementById('statsContainer');
    
    headerRow.innerHTML = '<th>加载中...</th>';
    tableBody.innerHTML = '<tr><td class="p-8 text-center text-gray-500">查询失败</td></tr>';
    statsContainer.classList.add('hidden');
}

/**
 * 显示状态消息
 */
function showStatus(type, message) {
    const container = document.getElementById('statusContainer');
    container.className = type === 'error' ? 'error-message' : 'success-message';
    container.textContent = message;
    container.classList.remove('hidden');
    
    // 3秒后自动隐藏成功消息
    if (type === 'success') {
        setTimeout(() => {
            container.classList.add('hidden');
        }, 3000);
    }
    
    console.log(`[${type.toUpperCase()}] ${message}`);
}

