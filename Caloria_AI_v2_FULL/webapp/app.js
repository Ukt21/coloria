console.log('placeholder');
const tg = window.Telegram.WebApp;
tg.expand();


async function loadData() {
    const userId = tg.initDataUnsafe?.user?.id;

    const stats = await fetch(`/api/stats/today/${userId}`).then(r => r.json());
    const tip = await fetch(`/api/ai/tip/${userId}`).then(r => r.json());

    drawCaloriesRing(stats.total.calories, stats.daily_goal_calories);
    drawBJURing(
        stats.total.protein + stats.total.fat + stats.total.carbs,
        stats.daily_goal_protein + stats.daily_goal_fat + stats.daily_goal_carbs
    );

    document.getElementById("calorieText").textContent =
        `${Math.round(stats.total.calories)} / ${Math.round(stats.daily_goal_calories)} ккал`;

    document.getElementById("bjuText").textContent =
        `${Math.round(stats.total.protein)} / ${Math.round(stats.daily_goal_protein)} • ` +
        `${Math.round(stats.total.fat)} / ${Math.round(stats.daily_goal_fat)} • ` +
        `${Math.round(stats.total.carbs)} / ${Math.round(stats.daily_goal_carbs)}`;

    buildFoodList(stats.entries);
    document.getElementById("aiTip").textContent = tip.tip;
}


// ---------------- RINGS ------------------
function drawRing(canvasId, value, max, color) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext("2d");

    const center = canvas.width / 2;
    const radius = 80;
    const lineWidth = 12;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.lineWidth = lineWidth;

    // background ring
    ctx.strokeStyle = "rgba(255,255,255,0.25)";
    ctx.beginPath();
    ctx.arc(center, center, radius, 0, Math.PI * 2);
    ctx.stroke();

    // progress ring
    let progress = value / max;
    if (progress > 1) progress = 1;

    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.arc(center, center, radius, -Math.PI / 2, (Math.PI * 2 * progress) - Math.PI / 2);
    ctx.stroke();
}

function drawCaloriesRing(value, max) {
    drawRing("calorieRing", value, max, "#ff3cd7");
}

function drawBJURing(value, max) {
    drawRing("bjuRing", value, max, "#bc3cff");
}


// ---------------- FOOD LIST ------------------
function buildFoodList(entries) {
    const list = document.getElementById("foodList");
    list.innerHTML = "";

    if (entries.length === 0) {
        list.innerHTML = "<i>Сегодня вы ещё ничего не записали</i>";
        return;
    }

    entries.forEach(e => {
        const item = document.createElement("div");
        item.className = "food-item";
        item.innerHTML = `
            <b>${e.text}</b><br>
            <small>${Math.round(e.calories)} ккал • 
            Б:${Math.round(e.protein)} 
            Ж:${Math.round(e.fat)} 
            У:${Math.round(e.carbs)}</small>
        `;
        list.appendChild(item);
    });
}

loadData();
