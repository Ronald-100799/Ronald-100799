      // ---------- custom layer (reel 10 v2, Terrace): one frame size throughout, zooms inside it; cute, quiet doodles ----------
      (function () {
        // same picture band for the whole reel (Ron's first 5 s are cropped to match the rest)
        tl.set("#fx", { clipPath: "inset(656px 0px 657px 0px)" }, 0);

        function drop(sel, t, rot) {
          tl.fromTo(sel, { opacity: 0, y: -50, rotation: rot * 3 }, { opacity: 1, y: 0, rotation: rot, duration: 0.55, ease: "back.out(2)" }, t);
          tl.fromTo(sel, { rotation: rot }, { rotation: rot * 0.6, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false }, t + 0.55);
        }
        const leave = (sel, t) => tl.to(sel, { opacity: 0, y: -30, scale: 0.95, duration: 0.25, ease: "power2.in" }, t);
        const show = (sel, t, y = 16) => tl.fromTo(sel, { opacity: 0, y }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, t);
        const hide = (sel, t) => tl.to(sel, { opacity: 0, duration: 0.2, ease: "power1.in" }, t);
        const twinkle = (sel, t, n = 3) => tl.fromTo(sel, { scale: 0, rotation: 0, opacity: 0 }, { scale: 1, rotation: 90, opacity: 1, duration: 0.35, ease: "back.out(2.5)", yoyo: true, repeat: n, repeatDelay: 0.25 }, t);

        // opening polaroids
        drop("#pA0", 0.05, -5); drop("#pA2", 1.6, 4);
        twinkle("#sA0", 0.6); twinkle("#sA1", 2.0);
        leave("#pA0", 4.62); leave("#pA2", 4.7);

        // ---- weight-gain doodles (no sound) ----
        ["#dT1", "#dT2", "#dCk", "#dG", "#dK", "#dK2", "#dK3", "#dP", "#dSw", "#dH", "#dHt"].forEach((s) => tl.set(s, { opacity: 0 }, 9.3));
        tl.fromTo("#dSc", { opacity: 0, scale: 0.6, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "back.out(2)" }, 9.32);
        tl.fromTo("#dNd", { rotation: -40 }, { rotation: -10, duration: 1.4, ease: "back.out(1.5)" }, 10.9);        // "gain a little weight"
        show("#dT1", 11.8);
        hide("#dT1", 12.7); show("#dT2", 12.85);                                                                     // "that's normal"
        tl.fromTo("#dCk path", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, 12.9);
        tl.set("#dCk", { opacity: 1 }, 12.9);
        hide(["#dT2", "#dCk"], 13.5);
        show("#dG", 13.7); hide("#dG", 15.5);                                                                          // "the good news…"
        tl.to("#dSc", { x: -300, scale: 0.75, duration: 0.5, ease: "power2.inOut" }, 17.2);                             // make room for the note
        tl.fromTo("#dK", { opacity: 0, scale: 0.7, rotation: -4 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.45, ease: "back.out(2)" }, 17.66);
        show("#dK2", 17.95, 10); show("#dK3", 18.1, 10);
        tl.fromTo("#dK", { rotation: -2 }, { rotation: 2, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false }, 18.2);
        hide(["#dK", "#dK2", "#dK3"], 19.9);
        tl.to("#dSc", { x: 0, scale: 1, duration: 0.5, ease: "power2.inOut" }, 20.2);
        tl.to("#dNd", { rotation: 55, duration: 0.35, ease: "back.out(3)" }, 22.11);                                  // "the scale goes up"
        tl.fromTo("#dSc", { x: 0 }, { keyframes: [{ x: -6, duration: 0.05 }, { x: 6, duration: 0.05 }, { x: -4, duration: 0.05 }, { x: 0, duration: 0.05 }], immediateRender: false }, 22.3);
        tl.fromTo("#dP", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, 22.89);   // panic
        tl.fromTo("#dSw", { opacity: 0, y: -10 }, { opacity: 1, y: 14, duration: 0.6, ease: "power1.in" }, 22.95);
        hide(["#dP", "#dSw"], 23.8);
        tl.to("#dSc", { opacity: 0, scale: 0.8, duration: 0.25 }, 23.8);
        show("#dHt", 23.9); tl.fromTo("#dH", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, 23.95);
        ["#dH0", "#dH1", "#dH2"].forEach((h, i) => tl.to(h, { y: 260, rotation: (i - 1) * 25, opacity: 0, duration: 0.8, ease: "power2.in" }, 25.0 + i * 0.35));   // "…drop them"
        hide("#dHt", 26.6);

        // protein first
        drop("#pE0", 32.9, 3); leave("#pE0", 35.75);
      })();
