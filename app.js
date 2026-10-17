/**
 * BrightCHAMPS USA Q4 Growth Prototype
 * Component: Dynamic Landing Page, Geo-Personalization, SMS OTP & Instant Calendar Lock
 * Author: Bharanee B (AI Associate, Founder's Office)
 * Stakeholder: Yatharth Sahoo (Senior Lead, Founder's Office)
 */

document.addEventListener("DOMContentLoaded", function () {
    // -------------------------------------------------------------------------
    // 1. AUTO-MAP UTM / AD-SET TO GEO VARIANT (WITH ?geo= OVERRIDE)
    // -------------------------------------------------------------------------
    const urlParams = new URLSearchParams(window.location.search);
    let resolvedGeo = "tech"; // default

    const explicitGeo = urlParams.get("geo");
    const utmContent = (urlParams.get("utm_content") || "").toLowerCase();
    const utmCampaign = (urlParams.get("utm_campaign") || "").toLowerCase();
    const adsetName = (urlParams.get("adset_name") || urlParams.get("utm_term") || "").toLowerCase();
    const allQueryStrings = `${utmContent} ${utmCampaign} ${adsetName}`;

    if (explicitGeo) {
        resolvedGeo = explicitGeo.toLowerCase();
    } else if (allQueryStrings.includes("suburban") || allQueryStrings.includes("frisco") || 
               allQueryStrings.includes("alpharetta") || allQueryStrings.includes("cary") || 
               allQueryStrings.includes("naperville") || allQueryStrings.includes("tier2")) {
        resolvedGeo = "suburban";
    } else if (allQueryStrings.includes("heartland") || allQueryStrings.includes("inland") || 
               allQueryStrings.includes("midwest") || allQueryStrings.includes("scholarship") || 
               allQueryStrings.includes("tier3")) {
        resolvedGeo = "heartland";
    } else if (allQueryStrings.includes("tech") || allQueryStrings.includes("diaspora") || 
               allQueryStrings.includes("bayarea") || allQueryStrings.includes("silicon") || 
               allQueryStrings.includes("seattle") || allQueryStrings.includes("austin") || 
               allQueryStrings.includes("tier1")) {
        resolvedGeo = "tech";
    }

    const geoConfigs = {
        tech: {
            badge: "Personalized for Silicon Valley, Seattle & Austin Tech Families",
            headline: "Turn Passive Screen Time Into <span class='gradient-text'>Real AI & Coding Superpowers.</span>",
            subtext: "Silicon Valley curriculum for ages 6–16. Watch your child build machine learning models, autonomous bots, and real Python algorithms with 1-on-1 elite mentors.",
            quote: "\"My 10-year-old was obsessed with Roblox. Within 3 weeks of BrightCHAMPS, he was writing real Python scripts to build his own games. Worth every penny.\"",
            author: "— Anita S., Software Engineering Director • Sunnyvale, CA",
            defaultState: "CA"
        },
        suburban: {
            badge: "Top-Rated 1-on-1 STEM Enrichment for Competitive Academic Corridors",
            headline: "Give Your Child the <span class='gradient-text'>Competitive STEM & Logic Edge.</span>",
            subtext: "The modern alternative to commute-heavy learning centers. Personalized 1-on-1 coding, AI, and math logic from top educators—from the comfort of home.",
            quote: "\"We used to spend 45 minutes driving to a coding franchise twice a week. BrightCHAMPS 1-on-1 format is 10x better quality, personalized, and saves our family hours.\"",
            author: "— Dr. Marcus V., Cardiologist & Parent • Frisco, TX",
            defaultState: "TX"
        },
        heartland: {
            badge: "World-Class 1-on-1 STEM Mentors Available Across All 50 States",
            headline: "Bring Silicon Valley Tech Mentors <span class='gradient-text'>Right to Your Living Room.</span>",
            subtext: "Affordable, engaging, and flexible 1-on-1 coding classes for ages 6–16. Claim your complimentary trial class and Q4 winter holiday scholarship voucher.",
            quote: "\"There are no robotics or coding clubs near our small town. BrightCHAMPS gave my daughter access to incredible mentors who inspire her every single week.\"",
            author: "— Sarah T., Educator & Homeschool Parent • Carmel, IN",
            defaultState: "IN"
        }
    };

    const activeConfig = geoConfigs[resolvedGeo] || geoConfigs.tech;

    document.getElementById("geo-badge-text").textContent = activeConfig.badge;
    document.getElementById("hero-headline").innerHTML = activeConfig.headline;
    document.getElementById("hero-subtext").textContent = activeConfig.subtext;
    document.querySelector(".quote-body").textContent = activeConfig.quote;
    document.querySelector(".quote-author").innerHTML = `<strong>${activeConfig.author}</strong>`;
    
    const stateSelect = document.getElementById("parent-state");
    if (stateSelect && activeConfig.defaultState) {
        stateSelect.value = activeConfig.defaultState;
    }

    // -------------------------------------------------------------------------
    // 2. DYNAMIC CURRICULUM RECOMMENDATION ENGINE (Step 1)
    // -------------------------------------------------------------------------
    const childAgeEl = document.getElementById("child-age");
    const codingExpEl = document.getElementById("coding-experience");
    const learningGoalEl = document.getElementById("learning-goal");
    const trackTitleEl = document.getElementById("matched-track-title");
    const trackDescEl = document.getElementById("matched-track-desc");
    const laptopAccessEl = document.getElementById("has-laptop-access");

    function updateMatchedTrack() {
        const age = parseInt(childAgeEl.value) || 10;
        const exp = codingExpEl.value;
        const goal = learningGoalEl.value;

        if (age <= 8) {
            trackTitleEl.textContent = "Junior AI Explorer & Visual Logic (Ages 6-8)";
            trackDescEl.textContent = "Hands-on creative animations, visual algorithms, and interactive storytelling.";
        } else if (age >= 13 || exp === "TEXT") {
            trackTitleEl.textContent = "Advanced Python, Algorithms & Machine Learning (Ages 13+)";
            trackDescEl.textContent = "Syntax-based coding, real-world data structures, and building GenAI voice agents.";
        } else if (goal === "GAME_DEV" || exp === "ROBLOX") {
            trackTitleEl.textContent = "Game Architecture & 3D Interactive Design";
            trackDescEl.textContent = "Physics engines, character logic, and publishing a playable game in 45 minutes.";
        } else {
            trackTitleEl.textContent = "Next-Gen AI & Python Creator Track (Ages 9-12)";
            trackDescEl.textContent = "Interactive project: Build a working smart assistant and math game in Python.";
        }
    }

    childAgeEl.addEventListener("change", updateMatchedTrack);
    codingExpEl.addEventListener("change", updateMatchedTrack);
    learningGoalEl.addEventListener("change", updateMatchedTrack);

    // -------------------------------------------------------------------------
    // 3. STEP PROGRESSION LOGIC
    // -------------------------------------------------------------------------
    const step1Content = document.getElementById("step-1-content");
    const step2Content = document.getElementById("step-2-content");
    const step3Content = document.getElementById("step-3-content");

    const tab1 = document.getElementById("step-tab-1");
    const tab2 = document.getElementById("step-tab-2");
    const tab3 = document.getElementById("step-tab-3");
    const conn1 = document.getElementById("connector-1");
    const conn2 = document.getElementById("connector-2");

    let leadData = {
        is_phone_verified: false,
        mock_otp: "123456"
    };

    // Step 1 -> Step 2
    document.getElementById("btn-next-step-1").addEventListener("click", function () {
        const childName = document.getElementById("child-name").value.trim();
        if (!childName) {
            alert("Please enter your child's first name to customize their project.");
            document.getElementById("child-name").focus();
            return;
        }

        leadData.child_name = childName;
        leadData.child_age = childAgeEl.value;
        leadData.has_laptop_access = laptopAccessEl.value === "YES";
        leadData.coding_experience = codingExpEl.value;
        leadData.learning_goal = learningGoalEl.value;
        leadData.matched_track = trackTitleEl.textContent;

        step1Content.classList.add("hidden");
        step2Content.classList.remove("hidden");

        tab1.classList.remove("active");
        tab1.classList.add("completed");
        conn1.classList.add("active");
        tab2.classList.add("active");
    });

    // Step 2 -> Step 1 (Back)
    document.getElementById("btn-back-step-2").addEventListener("click", function () {
        step2Content.classList.add("hidden");
        step1Content.classList.remove("hidden");

        tab2.classList.remove("active");
        conn1.classList.remove("active");
        tab1.classList.remove("completed");
        tab1.classList.add("active");
    });

    // -------------------------------------------------------------------------
    // 4. MOCK SMS OTP VERIFICATION (Twilio Verify Architecture)
    // -------------------------------------------------------------------------
    const btnSendOtp = document.getElementById("btn-send-otp");
    const otpContainer = document.getElementById("otp-container");
    const otpInput = document.getElementById("otp-input");
    const btnVerifyOtp = document.getElementById("btn-verify-otp");
    const otpStatusMsg = document.getElementById("otp-status-msg");
    const phoneInput = document.getElementById("parent-phone");

    btnSendOtp.addEventListener("click", function () {
        const phone = phoneInput.value.replace(/\D/g, "");
        if (phone.length < 10) {
            alert("Please enter a valid 10-digit US phone number first.");
            phoneInput.focus();
            return;
        }

        otpContainer.classList.remove("hidden");
        otpInput.value = "123456"; // Auto-fill mock verification code
        btnSendOtp.textContent = "Resend SMS";
        otpStatusMsg.innerHTML = "✅ SMS Code sent! Twilio Sandbox: Verification code <strong>123456</strong> ready.";
        otpStatusMsg.style.color = "#16A34A";
    });

    btnVerifyOtp.addEventListener("click", function () {
        const code = otpInput.value.trim();
        if (code === leadData.mock_otp || code.length === 6) {
            leadData.is_phone_verified = true;
            otpStatusMsg.innerHTML = "✓ Phone number verified successfully (+1 " + phoneInput.value + ")";
            otpStatusMsg.style.color = "#15803D";
            btnVerifyOtp.textContent = "Verified ✓";
            btnVerifyOtp.style.background = "#15803D";
            btnSendOtp.style.display = "none";
        } else {
            alert("Invalid verification code. Please enter 123456 for testing.");
        }
    });

    // -------------------------------------------------------------------------
    // 5. STEP 2 SUBMIT & TCPA VALIDATION
    // -------------------------------------------------------------------------
    document.getElementById("btn-submit-lead").addEventListener("click", function () {
        const pfName = document.getElementById("parent-fname").value.trim();
        const plName = document.getElementById("parent-lname").value.trim();
        const pEmail = document.getElementById("parent-email").value.trim();
        const pPhone = document.getElementById("parent-phone").value.trim();
        const pState = document.getElementById("parent-state").value;
        const pZip = document.getElementById("parent-zip").value.trim();
        const tcpaChecked = document.getElementById("tcpa-consent").checked;

        if (!pfName || !plName) {
            alert("Please provide the parent first and last name.");
            return;
        }
        if (!pEmail || !pEmail.includes("@")) {
            alert("Please provide a valid parent email address.");
            return;
        }
        if (!pPhone || pPhone.replace(/\D/g, "").length < 10) {
            alert("Please provide a valid 10-digit US mobile phone number.");
            return;
        }
        if (!tcpaChecked) {
            alert("Please check the TCPA communication consent checkbox to proceed.");
            return;
        }

        leadData.parent_first_name = pfName;
        leadData.parent_last_name = plName;
        leadData.email = pEmail;
        leadData.phone = pPhone;
        leadData.state = pState;
        leadData.zip_code = pZip;
        leadData.tcpa_consent = true;
        leadData.lead_id = "US-LEAD-" + Math.floor(100000 + Math.random() * 900000);

        // Transition to Step 3 (Calendar Lock)
        step2Content.classList.add("hidden");
        step3Content.classList.remove("hidden");

        tab2.classList.remove("active");
        tab2.classList.add("completed");
        conn2.classList.add("active");
        tab3.classList.add("active");

        document.getElementById("confirmation-header").textContent = 
            `Class Pass Confirmed for ${leadData.child_name}!`;

        renderAvailableSlots();
    });

    // -------------------------------------------------------------------------
    // 6. INSTANT DEMO SLOT PICKER & GOOGLE CALENDAR SYNC (Step 3)
    // -------------------------------------------------------------------------
    function renderAvailableSlots() {
        const container = document.getElementById("slots-container");
        container.innerHTML = "";

        const now = new Date();
        const tomorrow = new Date(now);
        tomorrow.setDate(now.getDate() + 1);
        const dayAfter = new Date(now);
        dayAfter.setDate(now.getDate() + 2);

        const options = [
            {
                label: `Tomorrow (${tomorrow.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}) at 5:00 PM EST`,
                startDt: new Date(tomorrow.setHours(17, 0, 0, 0)),
                badge: "MOST POPULAR"
            },
            {
                label: `Tomorrow (${tomorrow.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}) at 7:00 PM EST`,
                startDt: new Date(tomorrow.setHours(19, 0, 0, 0)),
                badge: "EVENING SLOT"
            },
            {
                label: `${dayAfter.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })} at 11:00 AM EST`,
                startDt: new Date(dayAfter.setHours(11, 0, 0, 0)),
                badge: "WEEKEND MORNING"
            }
        ];

        options.forEach((opt, idx) => {
            const card = document.createElement("div");
            card.className = "slot-option" + (idx === 0 ? " selected" : "");
            card.innerHTML = `
                <div class="slot-time">${opt.label}</div>
                <div class="slot-badge">${opt.badge}</div>
            `;

            card.addEventListener("click", () => {
                document.querySelectorAll(".slot-option").forEach(el => el.classList.remove("selected"));
                card.classList.add("selected");
                lockSelectedSlot(opt);
            });

            container.appendChild(card);
        });

        lockSelectedSlot(options[0]);
    }

    function lockSelectedSlot(slot) {
        const lockedCard = document.getElementById("locked-slot-card");
        const detailsEl = document.getElementById("locked-details-text");
        const gcalBtn = document.getElementById("btn-gcal-link");
        const icsBtn = document.getElementById("btn-ics-link");

        lockedCard.classList.remove("hidden");
        detailsEl.textContent = `${slot.label} with Senior STEM Mentor`;

        const child = leadData.child_name || "Child";
        const zoomLink = `https://brightchamps.zoom.us/j/${leadData.lead_id}`;

        const startIso = slot.startDt.toISOString().replace(/-|:|\.\d\d\d/g, "");
        const endDt = new Date(slot.startDt.getTime() + 45 * 60000);
        const endIso = endDt.toISOString().replace(/-|:|\.\d\d\d/g, "");

        const title = encodeURIComponent(`BrightCHAMPS 1-on-1 Trial Class - ${child}`);
        const details = encodeURIComponent(`Excited to meet ${child}!\nPlease join 5 minutes early using a laptop/computer.\nZoom Meeting Link: ${zoomLink}`);
        const location = encodeURIComponent(zoomLink);

        const gcalUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&dates=${startIso}/${endIso}&details=${details}&location=${location}`;
        gcalBtn.href = gcalUrl;

        const icsContent = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//BrightCHAMPS//Trial Concierge//EN",
            "BEGIN:VEVENT",
            `SUMMARY:BrightCHAMPS 1-on-1 Trial Class - ${child}`,
            `DESCRIPTION:Join with ${child} using laptop. Zoom: ${zoomLink}`,
            `DTSTART:${startIso}`,
            `DTEND:${endIso}`,
            `LOCATION:${zoomLink}`,
            "STATUS:CONFIRMED",
            "END:VEVENT",
            "END:VCALENDAR"
        ].join("\n");

        icsBtn.href = "data:text/calendar;charset=utf8," + encodeURIComponent(icsContent);
    }

    // Reschedule Button
    const btnReschedule = document.getElementById("btn-reschedule");
    if (btnReschedule) {
        btnReschedule.addEventListener("click", function () {
            renderAvailableSlots();
            window.scrollTo({ top: document.querySelector(".slot-picker-wrap").offsetTop - 50, behavior: "smooth" });
        });
    }
});
