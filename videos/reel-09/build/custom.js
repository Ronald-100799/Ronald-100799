      // ---------- custom layer (reel 09): straight cuts in/out of blocks; only the content inside animates ----------
      (function () {
        const IN = "expo.out", SET = "back.out(1.7)", OUT = "power2.in";
        const pop = (sel, t, from = 0.6) => tl.fromTo(sel, { opacity: 0, scale: from }, { opacity: 1, scale: 1, duration: 0.28, ease: SET }, t);
        const rise = (sel, t, y = 30) => tl.fromTo(sel, { opacity: 0, y }, { opacity: 1, y: 0, duration: 0.3, ease: IN }, t);
        const away = (sel, t) => tl.to(sel, { opacity: 0, y: -14, duration: 0.15, ease: OUT }, t);

        // Ron's own screenshot / text box: re-laid from the graded footage above the caption shade (see custom.html)
        // hook: point A -> point B
        pop("#o1a", 1.15); tl.fromTo("#o1p", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.35, ease: "power2.inOut" }, 1.98); pop("#o1b", 2.18);
        away("#o1 .band", 3.36);
        // use / abuse / overuse
        pop("#o2a", 15.4); pop("#o2b", 15.94); pop("#o2c", 16.52, 0.4);
        away("#o2 .band", 17.38);

        // BLOCK A: bro-science or real results?
        tl.fromTo("#bkA .kk", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: IN }, 19.1);
        tl.fromTo("#aA", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, 19.18);
        rise("#aV", 20.4, 16);
        tl.fromTo("#aB", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, 21.02);
        tl.to("#aA", { opacity: 0.4, duration: 0.25 }, 21.1);
        // scene 2 inside the same backdrop, on Ron's words: "In 2018 researchers" / "30 untrained men"; then a straight cut to his screenshot at 24.4
        tl.to("#aS1", { opacity: 0, y: -30, duration: 0.2, ease: OUT }, 22.7);
        tl.fromTo("#aS2", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 22.86);
        tl.fromTo("#aS2k", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: IN }, 22.86);
        tl.fromTo("#aS2n", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.28, ease: "power4.out" }, 23.9);
        tl.fromTo("#aS2t", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: IN }, 24.12);

        // groups (top band while Ron explains)
        tl.fromTo("#o3a", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: IN }, 27.34);
        tl.fromTo("#o3b", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: IN }, 31.33);
        away("#o3 .band", 34.32);

        // BLOCK C: result bars (3D in custom.mjs), labels
        rise("#bkC .kk", 37.22, 16); rise("#bkC .sm", 37.35, 12);
        rise("#cL0", 38.1, 16); rise("#cL1", 37.9, 16);
        tl.fromTo("#cL0 b", { scale: 1.3 }, { scale: 1, duration: 0.25, ease: SET }, 39.15);
        tl.fromTo("#bkC .src", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 39.5);

        // BLOCK D: limitations
        tl.fromTo("#bkD .mid", { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, 45.97);
        rise("#dR0", 47.93); tl.fromTo("#dR0 .b", { opacity: 0, x: 20 }, { opacity: 1, x: 0, duration: 0.25, ease: IN }, 49.01);
        tl.fromTo("#bkD .src", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 49.3);

        // limitations recap after Ron's own text box
        pop("#o4a", 55.3); pop("#o4b", 55.6); pop("#o4c", 55.95, 0.4);
        away("#o4 .band", 56.9);
      })();
