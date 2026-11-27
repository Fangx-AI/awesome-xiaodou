"use strict";

const scenarios = {
  weight: {
    goal: "想养成更容易坚持的饮食习惯，工作日午饭常点外卖。",
    first: "打开常点的一家外卖店，选出一个今天能点的主食、蛋白质和蔬菜组合。",
    later: "看昨天或今天的记录，选一个下次点餐也容易重复的搭配。",
    lighter: "先把常点的一家店或菜单记下来，下一餐再从里面选。"
  },
  video: {
    goal: "月底之前剪出一条 60 秒的短视频。",
    first: "定一句视频要讲的话，把两段能支持主题的素材放进同一个文件夹。",
    later: "用现有素材粗剪前 10 秒，确认观众能看出主题。",
    lighter: "只写一句开头，并标记最可能用到的一段素材。"
  },
  meet: {
    goal: "这周约两位朋友在同一个商圈吃饭。",
    first: "选一个双方大致方便的时间段和一个商圈，写下人均预算。",
    later: "写一条邀约草稿，包含两个备选时间和大致地点，发之前再核对。",
    lighter: "先写下你自己能去的一个时间和商圈。"
  },
  custom: {
    goal: "",
    first: "写一句「做到什么就算成」，再准备一个能立刻打开的文件或材料。",
    later: "把刚完成的成果打开，补一个最小可验证的缺口。",
    lighter: "圈出一个最卡的点，写下解决它需要的一个信息。"
  }
};

const key = "xiaodou-studio-v1";
const reviewAction = "回看已做的事，写下下一次应该保留的一点和剩下的未完成事项。";
const el = (id) => document.getElementById(id);
let storageAvailable = true;
function load() {
  try {
    const value = JSON.parse(localStorage.getItem(key));
    return value && Object.hasOwn(scenarios, value.scene) && value.plans && typeof value.plans === "object"
      ? { ...value, archives: Array.isArray(value.archives) ? value.archives : [] }
      : {scene:"weight", plans:{}, archives:[]};
  } catch {
    return {scene:"weight", plans:{}, archives:[]};
  }
}
let state = load();

function save() {
  try { localStorage.setItem(key, JSON.stringify(state)); }
  catch { storageAvailable = false; }
}
function flash(message) {
  el("feedback").textContent = storageAvailable ? message : message + " 浏览器无法保存，请复制进度。";
}
function current() {
  return state.plans[state.scene];
}
function candidate(plan) {
  const scene = scenarios[state.scene];
  const last = plan.history.at(-1);
  if (last?.result === "done" && last.action === reviewAction) return "";
  if (last?.result === "blocked") return scene.lighter;
  const completed = plan.history.filter(entry => entry.result === "done").length;
  if (completed >= 2) return reviewAction;
  if (plan.minutes === 5) return scene.lighter;
  return completed ? scene.later : scene.first;
}
function showTask() {
  const plan = current();
  el("empty").hidden = !!plan;
  el("task").hidden = !plan;
  el("export").hidden = true;
  el("note").value = plan?.note ?? "";
  if (!plan) return;
  el("action").value = plan.action;
  el("action").placeholder = plan.action ? "" : "这一轮已回顾。准备好时，写一个新的下一步。";
  el("task-meta").textContent = plan.goal + " · 今天有 " + plan.minutes + " 分钟";
  const list = el("history-list");
  list.replaceChildren();
  el("history").hidden = !plan.history.length;
  for (const entry of [...plan.history].reverse()) {
    const item = document.createElement("li");
    item.textContent = (entry.result === "done" ? "本人回报完成" : "本人回报卡住") + "：" + entry.action + (entry.note ? " · 备注：" + entry.note : "");
    list.append(item);
  }
}
function showArchives() {
  el("archives").hidden = !state.archives.length;
  const list = el("archive-list");
  list.replaceChildren();
  for (const plan of [...state.archives].reverse()) {
    const row = document.createElement("li");
    const details = document.createElement("details");
    const title = document.createElement("summary");
    title.textContent = plan.goal;
    const note = document.createElement("p");
    note.textContent = "归档时下一步：" + (plan.action || "待定");
    const history = document.createElement("ul");
    for (const entry of plan.history) {
      const item = document.createElement("li");
      item.textContent = (entry.result === "done" ? "完成：" : "卡住：") + entry.action + (entry.note ? " · " + entry.note : "");
      history.append(item);
    }
    details.append(title, note, history);
    row.append(details);
    list.append(row);
  }
}
function select(scene) {
  state.scene = scene;
  for (const button of document.querySelectorAll("[data-scenario]")) {
    button.setAttribute("aria-pressed", String(button.dataset.scenario === scene));
  }
  el("goal").value = current()?.goal ?? scenarios[scene].goal;
  el("capacity").value = String(current()?.minutes ?? 15);
  el("feedback").textContent = "";
  showTask();
}
for (const button of document.querySelectorAll("[data-scenario]")) {
  button.addEventListener("click", () => { select(button.dataset.scenario); save(); });
}
el("plan-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const goal = el("goal").value.trim();
  if (!goal) { flash("先写一句想做成什么。"); el("goal").focus(); return; }
  const minutes = Number(el("capacity").value);
  const previous = current();
  const history = previous?.goal === goal ? previous.history : [];
  if (previous && previous.goal !== goal && previous.history.length) {
    flash("这件事已有进度。可以保留原目标调整时间，或用「归档并开启新目标」。");
    return;
  }
  const same = previous?.goal === goal && previous.minutes === minutes;
  const plan = {goal, minutes, history, note: previous?.goal === goal ? previous.note ?? "" : ""};
  plan.action = same ? previous.action : candidate(plan);
  state.plans[state.scene] = plan;
  save();
  showTask();
  flash(same ? "正在显示当前这一步。" : "下一步已就绪，可以直接改成适合你的做法。");
});
el("action").addEventListener("input", () => {
  if (!current()) return;
  current().action = el("action").value;
  save();
});
el("note").addEventListener("input", () => {
  if (!current()) return;
  current().note = el("note").value;
  save();
});
el("archive").addEventListener("click", () => {
  const plan = current();
  if (!plan) return;
  state.archives.push(plan);
  delete state.plans[state.scene];
  save();
  select(state.scene);
  showArchives();
  el("goal").value = "";
  el("goal").focus();
  flash("已归档，历史记录可在下方查看。现在可以写新目标。");
});
for (const button of document.querySelectorAll("[data-result]")) {
  button.addEventListener("click", () => {
    const plan = current();
    const action = el("action").value.trim();
    if (!plan || !action) { flash("请先填入你正在做的一步。"); el("action").focus(); return; }
    plan.history.push({result:button.dataset.result, action, note:el("note").value.trim()});
    plan.note = "";
    plan.action = candidate(plan);
    save();
    showTask();
    if (!plan.action) flash("本轮已回顾。可以复制进度到小豆，也可以写下新的下一步。");
    else flash(button.dataset.result === "done" ? "已记下你完成的事，下一步已更新。" : "已记下卡点，换成更容易开始的一步。");
  });
}
el("copy").addEventListener("click", async () => {
  const plan = current();
  const notes = plan.history.length ? plan.history.slice(-6).map(entry =>
    "- " + (entry.result === "done" ? "已完成" : "卡住") + "：" + entry.action + (entry.note ? "，" + entry.note : "")
  ).join("\n") : "暂未回报进展。";
  const draft = el("note").value.trim();
  const text = "你是我的小豆个人助理，默认称我皇上。按以下进度继续，用白话给一个下一步。\n\n目标：" + plan.goal
    + "\n手头时间：" + plan.minutes + " 分钟\n本人回报：\n" + notes + "\n当前下一步：" + (plan.action.trim() || "待定")
    + (draft ? "\n补充：" + draft : "") + "\n请保留已完成事项。涉及向外发送或更改资料时，先让我确认。";
  el("export-text").value = text;
  try {
    await navigator.clipboard.writeText(text);
    flash("已复制。打开小豆，把这段粘贴进去就能接着聊。");
  } catch {
    el("export").hidden = false;
    el("export").open = true;
    el("export-text").select();
    flash("请手动复制已选中的内容。");
  }
});

async function showRoles() {
  const target = el("roles");
  try {
    const response = await fetch("roles.json");
    if (!response.ok) throw new Error("roles unavailable");
    const roles = await response.json();
    for (const group of ["三省", "六部"]) {
      const section = document.createElement("section");
      section.className = "role-group";
      const heading = document.createElement("h3");
      heading.textContent = group;
      const list = document.createElement("div");
      list.className = "role-list";
      for (const role of roles.filter(row => row.group === group)) {
        const card = document.createElement("details");
        card.className = "role";
        const title = document.createElement("summary");
        const portrait = document.createElement("img");
        portrait.className = "portrait";
        portrait.src = "portraits/" + role.portrait;
        portrait.alt = "";
        portrait.loading = "lazy";
        portrait.width = 62;
        portrait.height = 62;
        const label = document.createElement("span");
        const name = document.createElement("strong");
        name.textContent = role.department + " · " + role.name;
        const duty = document.createElement("small");
        duty.textContent = role.duty;
        label.append(name, duty);
        title.append(portrait,label);
        const body = document.createElement("p");
        body.textContent = role.personality + "。负责" + role.deliverable + "。例如：" + role.example;
        card.append(title,body);
        list.append(card);
      }
      section.append(heading,list);
      target.append(section);
    }
  } catch {
    target.textContent = "暂时无法读取人物资料，仍可继续使用上方工作台。";
  }
}

select(state.scene);
showArchives();
showRoles();
