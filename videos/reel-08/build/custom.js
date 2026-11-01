      // ---------- custom layer (reel 08, v2: fewer, grouped cutaways with soft transitions) ----------
      (function () {
        const IN = "expo.out", SET = "back.out(1.7)", OUT = "power2.in";
        const D = 0.32; // face <-> graphics dissolve length
        // Face -> block: the footage softens (blur + slight push) while the block dissolves in.
        // Block -> face: the block dissolves out while the footage sharpens. hard=true skips a side (movie cuts).
        function block(id, t0, t1, hardIn = false, hardOut = false) {
          if (hardIn) { tl.set(id, { opacity: 1 }, t0); tl.set("#fx", { filter: "blur(14px)" }, t0); }
          else {
            tl.fromTo(id, { opacity: 0, scale: 1.03 }, { opacity: 1, scale: 1, duration: D, ease: "power2.out" }, t0);
            tl.fromTo("#fx", { filter: "blur(0px)" }, { filter: "blur(14px)", duration: D, ease: "power1.in", immediateRender: false }, t0 - 0.08);
          }
          if (hardOut) { tl.set("#fx", { filter: "blur(0px)" }, t1); }
          else {
            tl.to(id, { opacity: 0, duration: D, ease: "power2.in" }, t1 - D);
            tl.fromTo("#fx", { filter: "blur(14px)" }, { filter: "blur(0px)", duration: D + 0.08, ease: "power1.out", immediateRender: false }, t1 - D);
          }
        }
        // scene switch inside a block (the dark backdrop stays, so it never cuts back through the face)
        const sceneIn = (id, t) => tl.fromTo(id, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: IN }, t);
        const sceneOut = (id, t) => tl.to(id, { opacity: 0, y: -30, duration: 0.2, ease: OUT }, t);
        const pop = (sel, t, from = 0.6) => tl.fromTo(sel, { opacity: 0, scale: from }, { opacity: 1, scale: 1, duration: 0.3, ease: SET }, t);
        const rise = (sel, t, y = 30) => tl.fromTo(sel, { opacity: 0, y }, { opacity: 1, y: 0, duration: 0.32, ease: IN }, t);
        const strikeX = (sel, t) => tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: 0.16, ease: "power3.out" }, t);
        const card = (id, t0, t1) => { tl.fromTo(id, { opacity: 0, y: -24 }, { opacity: 1, y: 0, duration: 0.35, ease: IN }, t0); tl.to(id, { opacity: 0, y: -16, duration: 0.25, ease: OUT }, t1 - 0.25); };

        // overlays while Ron talks
        pop("#oAc", 0.18); tl.to("#oAc", { opacity: 0, y: -14, duration: 0.15, ease: OUT }, 1.47);
        pop("#oB0", 1.62); strikeX("#oB0 .x", 1.85); pop("#oB1", 2.18); strikeX("#oB1 .x", 2.4);
        tl.to("#oB .band", { opacity: 0, duration: 0.2, ease: OUT }, 3.46);

        // BLOCK 1: semaglutide pen -> price slam over the riser; hard cut into the movie at 7.433
        block("#bk1", 3.66, 7.433, false, true);
        sceneIn("#s1a", 3.7);
        tl.fromTo("#s1aw", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: SET }, 4.28);
        sceneOut("#s1a", 5.2); sceneIn("#s1b", 5.38);
        tl.fromTo("#cDp", { scale: 1.25 }, { scale: 1, duration: 0.22, ease: "power4.out", immediateRender: false }, 6.22);
        tl.fromTo("#bk1g", { opacity: 0 }, { opacity: 0.35, duration: 0.15 }, 6.22);
        tl.to("#bk1g", { opacity: 0.9, duration: 1.1, ease: "power2.in" }, 6.3);
        tl.fromTo("#cDp", { scale: 1 }, { scale: 1.08, duration: 1.1, ease: "power1.in", immediateRender: false }, 6.3);
        rise("#cDs", 6.45, 16); tl.fromTo("#cDsrc", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 6.55);
        tl.fromTo("#s1b", { x: 0 }, { keyframes: [{ x: -12, duration: 0.04 }, { x: 10, duration: 0.04 }, { x: -5, duration: 0.04 }, { x: 0, duration: 0.04 }] }, 6.22);

        // hype meter
        pop("#oF0", 14.55); pop("#oF1", 15.54);
        tl.fromTo("#oFm", { scaleX: 0 }, { scaleX: 1, duration: 1.6, ease: "power2.in" }, 14.9);
        tl.to("#oF .cc", { opacity: 0, y: -14, duration: 0.15, ease: OUT }, 17.25);

        // BLOCK 2: off patent (padlock) -> price in India
        block("#bk2", 19.18, 24.88);
        sceneIn("#s2a", 19.25);
        tl.fromTo("#cHst", { opacity: 0, scale: 1.8, rotation: -14 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.22, ease: "power4.in" }, 20.62);
        tl.fromTo("#s2a", { x: 0 }, { keyframes: [{ x: 10, duration: 0.04 }, { x: -8, duration: 0.04 }, { x: 0, duration: 0.05 }], immediateRender: false }, 20.84);
        rise("#cHd", 21.05, 14);
        tl.fromTo("#cHv", { opacity: 1 }, { opacity: 0, duration: 0.2, immediateRender: false }, 21.56);
        sceneOut("#s2a", 21.58); sceneIn("#s2b", 21.76);
        tl.fromTo("#cIx", { scaleX: 0 }, { scaleX: 1, duration: 0.18, ease: "power3.out" }, 22.2);
        tl.to(["#cIb", "#cIbl"], { opacity: 0.45, duration: 0.2 }, 22.35);
        tl.fromTo("#cIg", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.28, ease: SET }, 22.9);
        rise("#cIgl", 23.1, 12);

        // BLOCK 3: STEP 1
        block("#bk3", 26.93, 31.11);
        sceneIn("#s3a", 26.98);
        tl.fromTo("#cKp", { rotation: -3 }, { rotation: -1.2, duration: 0.4, ease: IN }, 26.98);
        tl.fromTo("#cKp .hl", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.3, ease: IN }, 28.5);
        rise("#cKl0", 28.3, 16); rise("#cKl1", 28.0, 16);
        tl.fromTo("#cKv0", { scale: 1.3 }, { scale: 1, duration: 0.25, ease: SET }, 28.67);

        // BLOCK 4: 3 things (hard cut in from the movie clip, soft out to the face)
        block("#bk4", 34.333, 36.93, true, false);
        tl.set("#s4a", { opacity: 1 }, 34.333);
        pop("#cM0", 35.15, 0.4); pop("#cM1", 35.35, 0.4); pop("#cM2", 35.55, 0.4);
        tl.fromTo("#cMt", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: SET }, 35.6);

        // points tracker while Ron explains 1 and 2 (3 is the block below)
        tl.fromTo("#oP .row", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: IN }, 36.95);
        tl.to("#pt2", { borderColor: "#E10600", color: "#E10600", duration: 0.2 }, 37.48);
        tl.fromTo("#pt2", { scale: 1 }, { scale: 1.15, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }, 37.5);
        tl.to("#pt2", { borderColor: "rgba(255,255,255,0.35)", color: "rgba(255,255,255,0.55)", duration: 0.2 }, 40.5);
        [[0, 40.78, 46.0], [1, 46.0, 49.36]].forEach(([n, a, z]) => {
          tl.to("#pt" + n, { backgroundColor: "#E10600", borderColor: "#E10600", color: "#FFFFFF", scale: 1.1, duration: 0.2 }, a);
          tl.fromTo("#pl" + n, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, ease: IN }, a + 0.05);
          tl.to("#pt" + n, { backgroundColor: "rgba(11,11,12,0.72)", borderColor: "rgba(255,255,255,0.35)", color: "rgba(255,255,255,0.55)", scale: 1, duration: 0.15 }, z - 0.05);
          tl.to("#pl" + n, { opacity: 0, duration: 0.12 }, z - 0.1);
        });
        tl.to("#pt2", { backgroundColor: "#E10600", borderColor: "#E10600", color: "#FFFFFF", scale: 1.1, duration: 0.2 }, 49.1);

        // BLOCK 5: what the trial actually did
        block("#bk5", 49.36, 53.92);
        sceneIn("#s5a", 49.42);
        pop("#cP0", 50.0); pop("#cPo0", 50.9); pop("#cP1", 51.2); pop("#cPo1", 52.0); pop("#cP2", 52.3); pop("#cPo2", 52.9);
        tl.fromTo("#cP3", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.in" }, 53.05);

        // fact cards (Ron stays on screen)
        card("#oQc", 54.1, 57.7);
        pop("#oT0", 63.2); strikeX("#oT0 .x", 63.5); pop("#oT1", 64.05); strikeX("#oT1 .x", 64.3);
        tl.to("#oT .band", { opacity: 0, y: -14, duration: 0.15, ease: OUT }, 65.75);
        card("#oUc", 66.1, 70.8);
      })();
