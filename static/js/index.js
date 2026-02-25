let timerInterval
let timeLeft = 0
let floatingElements = []
let animationRunning = false
const textarea = document.getElementById("user-code-input")
const lineNumbers = document.getElementById("line-numbers")

function updateLineNumbers() {
    const lines = textarea.value.split("\n").length
    let html = ""
    for (let i = 1; i <= lines; i++) html += i + "<br>"
    lineNumbers.innerHTML = html
}

textarea.addEventListener("input", updateLineNumbers)
textarea.addEventListener("scroll", () => {
    lineNumbers.scrollTop = textarea.scrollTop
})

updateLineNumbers()
function generateStars(count = 80) {
    const area = document.getElementById("code-scatter-area")
    for (let i = 0; i < count; i++) {
        const star = document.createElement("div")
        star.className = "star"
        star.style.left = Math.random() * 100 + "%"
        star.style.top = Math.random() * 100 + "%"
        star.style.opacity = Math.random()
        area.appendChild(star)
    }
}
generateStars()

function lockEditor() {
    const textarea = document.getElementById("user-code-input")
    const submitBtn = document.getElementById("submit-button")

    textarea.readOnly = true
    submitBtn.disabled = true
    submitBtn.style.opacity = "0.6"
    submitBtn.style.cursor = "not-allowed"
}
document.getElementById("load-code-button").onclick = async () => {
    const code = document.getElementById("secret-code-input").value

    const res = await fetch("/load-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ secret_code: code })
    })

    const data = await res.json()
    if (!data.success) {
        document.getElementById("status-message").innerText = data.message
        return
    }

    const area = document.getElementById("code-scatter-area")
    area.innerHTML = ""
    generateStars()
    floatingElements = []

    const rect = area.getBoundingClientRect()

    data.code_elements.forEach(el => {
        const d = document.createElement("div")
        d.className = "code-element"
        d.innerText = el

        const x = Math.random() * (rect.width - 100)
        const y = Math.random() * (rect.height - 40)

        d.style.transform = `translate(${x}px, ${y}px)`
        area.appendChild(d)

        floatingElements.push({
            el: d,
            x: x,
            y: y,
            dx: (Math.random() - 0.5) * 0.35,
            dy: (Math.random() - 0.5) * 0.35
        })
    })

    clearInterval(timerInterval)
    timeLeft = data.time_limit
    startTimer()

    if (!animationRunning) {
        animationRunning = true
        animate()
    }
}

function animate() {
    const area = document.getElementById("code-scatter-area")
    const rect = area.getBoundingClientRect()

    for (let i = 0; i < floatingElements.length; i++) {
        const a = floatingElements[i]

        a.x += a.dx
        a.y += a.dy

        const maxX = rect.width - a.el.offsetWidth
        const maxY = rect.height - a.el.offsetHeight

        if (a.x <= 0 || a.x >= maxX) a.dx *= -1
        if (a.y <= 0 || a.y >= maxY) a.dy *= -1

        for (let j = i + 1; j < floatingElements.length; j++) {
            const b = floatingElements[j]

            const dx = a.x - b.x
            const dy = a.y - b.y
            const distance = Math.sqrt(dx * dx + dy * dy)

            if (distance < 60) {
                const force = 0.03
                const nx = dx / distance
                const ny = dy / distance

                a.dx += nx * force
                a.dy += ny * force
                b.dx -= nx * force
                b.dy -= ny * force
            }
        }

        a.el.style.transform = `translate(${a.x}px, ${a.y}px)`
    }

    requestAnimationFrame(animate)
}


async function submitCode(auto = false) {
    clearInterval(timerInterval)
    lockEditor()

    const code = document.getElementById("user-code-input").value

    const res = await fetch("/submit-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_code: code, time_taken: timeLeft })
    })

    const data = await res.json()
    document.getElementById("status-message").innerText =
        `Score: ${data.score}/${data.total}`
}

document.getElementById("submit-button").onclick = () => {
    submitCode(false)
}

function startTimer() {
    const timerEl = document.getElementById("timer-value")
    timerEl.innerText = timeLeft

    timerInterval = setInterval(() => {
        timeLeft--
        timerEl.innerText = timeLeft

        timerEl.className = ""

        if (timeLeft <= 10) {
            timerEl.classList.add("timer-red", "timer-pulse")
        } else if (timeLeft <= 30) {
            timerEl.classList.add("timer-yellow")
        } else {
            timerEl.classList.add("timer-green")
        }

        if (timeLeft <= 0) {
            clearInterval(timerInterval)
            submitCode(true)
        }
    }, 1000)
} 