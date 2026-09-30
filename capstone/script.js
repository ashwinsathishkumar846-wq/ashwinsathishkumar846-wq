// ---------- DATA ----------
const PASSWORD = 'Srec@2026';
const STUDENTS = {
  '71812401006': 'Aishwarya U',
  '71812401007': 'Ajay Iyanraj',
  '71812401008': 'Akashvarman R',
  '71812401009': 'Akhilesh Raj P'
};
const MAX_CREDITS = 24;
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
const PERIODS = ['9:00 - 10:00', '10:00 - 11:00', '11:15 - 12:15', '1:15 - 2:15', '2:15 - 3:15'];

// seats = total seats, taken = seats already occupied by other students
const COURSES = [
  { code: '20CS212', title: 'Web Technologies',        dept: 'CSE',  credits: 3, faculty: 'Mr. N. Manoj',   slots: ['Mon-1', 'Wed-2'], seats: 60, taken: 41 },
  { code: '20CS201', title: 'Data Structures',         dept: 'CSE',  credits: 4, faculty: 'Dr. S. Priya',   slots: ['Tue-1', 'Thu-1'], seats: 60, taken: 52 },
  { code: '20CS202', title: 'Database Management',     dept: 'CSE',  credits: 3, faculty: 'Ms. R. Kavitha', slots: ['Mon-3', 'Fri-2'], seats: 60, taken: 38 },
  { code: '20CS203', title: 'Operating Systems',       dept: 'CSE',  credits: 3, faculty: 'Dr. M. Suresh',  slots: ['Tue-2', 'Fri-1'], seats: 60, taken: 59 },
  { code: '20CS204', title: 'Computer Networks',       dept: 'CSE',  credits: 3, faculty: 'Mr. K. Arun',    slots: ['Mon-1', 'Thu-3'], seats: 60, taken: 30 },
  { code: '20CS205', title: 'Software Engineering',    dept: 'CSE',  credits: 3, faculty: 'Ms. L. Divya',   slots: ['Wed-3', 'Fri-4'], seats: 60, taken: 45 },
  { code: '20CS206', title: 'Artificial Intelligence', dept: 'AI&DS', credits: 4, faculty: 'Dr. V. Rajesh', slots: ['Tue-4', 'Thu-2'], seats: 40, taken: 40 },
  { code: '20CS207', title: 'Cyber Security',          dept: 'AI&DS', credits: 3, faculty: 'Mr. T. Harish', slots: ['Wed-4', 'Fri-3'], seats: 40, taken: 22 },
  { code: '20CS208', title: 'Cloud Computing',         dept: 'IT',   credits: 3, faculty: 'Ms. P. Anitha',  slots: ['Thu-4', 'Tue-3'], seats: 50, taken: 35 },
  { code: '20MA201', title: 'Discrete Mathematics',    dept: 'MATHS', credits: 4, faculty: 'Dr. G. Latha',  slots: ['Mon-2', 'Wed-1'], seats: 70, taken: 48 },
  { code: '20HS201', title: 'Professional Ethics',     dept: 'HSS',  credits: 2, faculty: 'Mr. B. Karthik', slots: ['Fri-5'],          seats: 80, taken: 50 },
  { code: '20CS279', title: 'Web Technologies Lab',    dept: 'CSE',  credits: 2, faculty: 'Mr. N. Manoj',   slots: ['Thu-5'],          seats: 60, taken: 44 }
];

// ---------- STORAGE (registrations of all students) ----------
let currentUser = null;
const store = {
  load() { try { return JSON.parse(localStorage.getItem('scrs')) || {}; } catch (e) { return {}; } },
  save(data) { localStorage.setItem('scrs', JSON.stringify(data)); }
};
const $ = id => document.getElementById(id);

function myCodes() { return store.load()[currentUser] || []; }
function courseByCode(code) { return COURSES.find(c => c.code === code); }
function seatsLeft(course) {
  const all = store.load();
  const mine = Object.values(all).filter(list => list.includes(course.code)).length;
  return course.seats - course.taken - mine;
}
function totalCredits() { return myCodes().reduce((sum, c) => sum + courseByCode(c).credits, 0); }

// ---------- TOAST ----------
let toastTimer;
function toast(msg, type) {
  const t = $('toast');
  t.textContent = msg; t.className = 'toast ' + type;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.add('hidden'), 3500);
}

// ---------- LOGIN / LOGOUT ----------
$('loginForm').addEventListener('submit', e => {
  e.preventDefault();
  const roll = $('roll').value.trim(), pwd = $('pwd').value;
  let msg = '';
  if (!/^\d{11}$/.test(roll)) msg = 'Roll number must contain exactly 11 digits.';
  else if (!STUDENTS[roll]) msg = 'Roll number not found.';
  else if (pwd.length < 8) msg = 'Password must be at least 8 characters.';
  else if (pwd !== PASSWORD) msg = 'Incorrect password. Please try again.';
  $('loginError').textContent = msg;
  if (msg) return;
  currentUser = roll;
  $('loginView').classList.add('hidden');
  $('appView').classList.remove('hidden');
  $('welcome').textContent = 'Welcome, ' + STUDENTS[roll] + ' (' + roll + ')';
  refreshAll();
});

$('logoutBtn').addEventListener('click', () => {
  currentUser = null;
  $('appView').classList.add('hidden');
  $('loginView').classList.remove('hidden');
  $('loginForm').reset();
});

// ---------- TABS ----------
document.querySelectorAll('.tab').forEach(btn => btn.addEventListener('click', () => {
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b === btn));
  document.querySelectorAll('.panel').forEach(p => p.classList.toggle('hidden', p.id !== btn.dataset.tab));
}));

// ---------- CATALOGUE ----------
[...new Set(COURSES.map(c => c.dept))].forEach(d => {
  const o = document.createElement('option'); o.value = o.textContent = d; $('deptFilter').appendChild(o);
});

function renderCatalogue() {
  const q = $('search').value.toLowerCase(), dept = $('deptFilter').value;
  const rows = COURSES.filter(c =>
    (dept === 'All' || c.dept === dept) &&
    (c.code + c.title + c.faculty).toLowerCase().includes(q));
  $('courseBody').innerHTML = rows.map(c => {
    const left = seatsLeft(c), done = myCodes().includes(c.code);
    const cls = left <= 0 ? 'full' : left <= 10 ? 'low' : 'ok';
    const btn = done ? '<button class="btn" disabled>Registered</button>'
      : left <= 0 ? '<button class="btn" disabled>Full</button>'
      : '<button class="btn primary" onclick="registerCourse(\'' + c.code + '\')">Register</button>';
    return '<tr><td>' + c.code + '</td><td>' + c.title + '</td><td>' + c.dept + '</td><td>' + c.credits +
      '</td><td>' + c.faculty + '</td><td>' + c.slots.join(', ') + '</td><td><span class="badge ' + cls + '">' +
      Math.max(left, 0) + '</span></td><td>' + btn + '</td></tr>';
  }).join('') || '<tr><td colspan="8">No courses match your search.</td></tr>';
}
$('search').addEventListener('input', renderCatalogue);
$('deptFilter').addEventListener('change', renderCatalogue);

// ---------- REGISTER / DROP ----------
function findClash(course) {
  for (const code of myCodes()) {
    const other = courseByCode(code);
    const shared = other.slots.find(s => course.slots.includes(s));
    if (shared) return { other, slot: shared };
  }
  return null;
}

function registerCourse(code) {
  const course = courseByCode(code), all = store.load();
  const clash = findClash(course);
  if (seatsLeft(course) <= 0) return toast(course.code + ' is full. No seats left.', 'error');
  if (totalCredits() + course.credits > MAX_CREDITS)
    return toast('Credit limit of ' + MAX_CREDITS + ' exceeded.', 'error');
  if (clash) return toast('Time clash with ' + clash.other.code + ' at ' + clash.slot + '.', 'error');
  all[currentUser] = [...myCodes(), code];
  store.save(all);
  toast('Registered for ' + course.code + ' - ' + course.title, 'success');
  refreshAll();
}

function dropCourse(code) {
  const all = store.load();
  all[currentUser] = myCodes().filter(c => c !== code);
  store.save(all);
  toast('Dropped ' + code, 'success');
  refreshAll();
}

// ---------- MY REGISTRATIONS ----------
function renderMine() {
  const list = myCodes().map(courseByCode), total = totalCredits();
  $('creditText').textContent = 'Credits registered: ' + total + ' / ' + MAX_CREDITS +
    '   |   Courses: ' + list.length;
  $('creditBar').style.width = (total / MAX_CREDITS * 100) + '%';
  $('myBody').innerHTML = list.map(c =>
    '<tr><td>' + c.code + '</td><td>' + c.title + '</td><td>' + c.credits + '</td><td>' + c.faculty +
    '</td><td>' + c.slots.join(', ') + '</td><td><button class="btn danger" onclick="dropCourse(\'' +
    c.code + '\')">Drop</button></td></tr>').join('') ||
    '<tr><td colspan="6">You have not registered for any course yet.</td></tr>';
}

// ---------- TIMETABLE ----------
function renderTimetable() {
  const slotMap = {};
  myCodes().map(courseByCode).forEach(c => c.slots.forEach(s => slotMap[s] = c.code));
  let html = '<tr><th>Period</th>' + DAYS.map(d => '<th>' + d + '</th>').join('') + '</tr>';
  PERIODS.forEach((time, p) => {
    html += '<tr><th>' + time + '</th>' + DAYS.map(d => {
      const code = slotMap[d + '-' + (p + 1)];
      return code ? '<td class="filled">' + code + '</td>' : '<td></td>';
    }).join('') + '</tr>';
  });
  $('ttTable').innerHTML = html;
}

function refreshAll() {
  $('creditChip').textContent = 'Credits: ' + totalCredits() + ' / ' + MAX_CREDITS;
  renderCatalogue(); renderMine(); renderTimetable();
}
