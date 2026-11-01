      // ---------- custom layer (reel 08) ----------
      (function () {
        const IN = "expo.out", SET = "back.out(1.7)", OUT = "power2.in";
        // cutaway entry: fast circular wipe from the centre; exit: quick scale-down fade (ends exactly at clip end)
        function cut(id, t0, t1, cut_out = true) {
          tl.fromTo(id, { clipPath: "circle(0% at 50% 42%)" }, { clipPath: "circle(120% at 50% 42%)", duration: 0.22, ease: "power3.out" }, t0);
          if (cut_out) tl.to(id, { opacity: 0, scale: 1.04, duration: 0.12, ease: OUT }, t1 - 0.12);
        }
        const pop = (sel, t, from = 0.6) => tl.fromTo(sel, { opacity: 0, scale: from }, { opacity: 1, scale: 1, duration: 0.3, ease: SET }, t);
        const rise = (sel, t, y = 30) => tl.fromTo(sel, { opacity: 0, y }, { opacity: 1, y: 0, duration: 0.32, ease: IN }, t);
        const strikeX = (sel, t) => tl.fromTo(sel, { scaleX: 0 }, { scaleX: 1, duration: 0.16, ease: "power3.out" }, t);
        const fadeOut = (sel, t) => tl.to(sel, { opacity: 0, y: -14, duration: 0.15, ease: OUT }, t);

        // A, B: overlays
        pop("#oAc", 0.18); fadeOut("#oAc", 1.47);
        pop("#oB0", 1.62); strikeX("#oB0 .x", 1.85); pop("#oB1", 2.18); strikeX("#oB1 .x", 2.4);
        tl.to("#oB .band", { scale: 0.9, opacity: 0, duration: 0.15, ease: OUT }, 3.5);

        // C: pen cutaway
        cut("#cC", 3.66, 5.38);
        rise("#cC .kk", 3.8); tl.fromTo("#cCw", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: SET }, 4.28);
        // D: price slam over the riser; hard cut into the movie clip at 7.433
        cut("#cD", 5.38, 7.433, false);
        rise("#cD .kk", 5.45);
        tl.fromTo("#cDp", { scale: 0.8 }, { scale: 1, duration: 0.5, ease: IN }, 5.55);
        tl.fromTo("#cDp", { scale: 1.25 }, { scale: 1, duration: 0.22, ease: "power4.out", immediateRender: false }, 6.22);
        tl.fromTo("#cDg", { opacity: 0 }, { opacity: 0.35, duration: 0.15 }, 6.22);
        tl.to("#cDg", { opacity: 0.9, duration: 1.1, ease: "power2.in" }, 6.3);
        tl.fromTo("#cDp", { scale: 1 }, { scale: 1.08, duration: 1.1, ease: "power1.in", immediateRender: false }, 6.3);
        rise("#cDs", 6.45, 16); tl.fromTo("#cDsrc", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 6.55);
        tl.fromTo("#cD .cc", { x: 0 }, { keyframes: [{ x: -12, duration: 0.04 }, { x: 10, duration: 0.04 }, { x: -5, duration: 0.04 }, { x: 0, duration: 0.04 }] }, 6.22);

        // F: hype meter
        pop("#oF0", 14.55); pop("#oF1", 15.54);
        tl.fromTo("#oFm", { scaleX: 0 }, { scaleX: 1, duration: 1.6, ease: "power2.in" }, 14.9);
        tl.fromTo("#oF .meter", { x: 0 }, { keyframes: [{ x: -6, duration: 0.04 }, { x: 6, duration: 0.04 }, { x: -3, duration: 0.04 }, { x: 0, duration: 0.04 }] }, 16.5);
        tl.to("#oF .cc", { opacity: 0, y: -14, duration: 0.15, ease: OUT }, 17.25);

        // H: off patent (padlock clip is a separate track on top)
        cut("#cH", 19.18, 21.76);
        rise("#cHk", 19.3); rise("#cHs", 20.0, 14);
        tl.fromTo("#cHst", { opacity: 0, scale: 1.8, rotation: -14 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.22, ease: "power4.in" }, 20.62);
        tl.fromTo("#cH .cc", { x: 0 }, { keyframes: [{ x: 10, duration: 0.04 }, { x: -8, duration: 0.04 }, { x: 0, duration: 0.05 }] }, 20.84);
        rise("#cHd", 21.05, 14);
        tl.to("#cHv", { opacity: 0, duration: 0.12 }, 21.64);
        // I: price in India
        cut("#cI", 21.76, 24.88);
        rise("#cI .kk", 21.85); rise("#cIb", 21.95); rise("#cIbl", 22.0, 12);
        tl.fromTo("#cIx", { scaleX: 0 }, { scaleX: 1, duration: 0.18, ease: "power3.out" }, 22.2);
        tl.to(["#cIb", "#cIbl"], { opacity: 0.45, duration: 0.2 }, 22.35);
        tl.fromTo("#cIg", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.28, ease: SET }, 22.9);
        rise("#cIgl", 23.1, 12); tl.fromTo("#cIsrc", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 23.3);

        // K: STEP 1 study
        cut("#cK", 26.93, 31.11);
        tl.fromTo("#cKp", { opacity: 0, y: 60, rotation: -3 }, { opacity: 1, y: 0, rotation: -1.2, duration: 0.4, ease: IN }, 27.0);
        tl.fromTo("#cKp .hl", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.3, ease: IN }, 28.5);
        rise("#cKl0", 28.3, 16); rise("#cKl1", 28.0, 16);
        tl.fromTo("#cKv0", { scale: 1.3 }, { scale: 1, duration: 0.25, ease: SET }, 28.67);

        // M: 3 things
        cut("#cM", 34.333, 36.93);
        rise("#cMk", 34.42);
        pop("#cM0", 35.15, 0.4); pop("#cM1", 35.35, 0.4); pop("#cM2", 35.55, 0.4);
        tl.fromTo("#cMt", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: SET }, 35.6);
        // points tracker: 3 pulses red on "the last one", then each point lights as it is spoken
        tl.fromTo("#oP .row", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: IN }, 36.95);
        tl.to("#pt2", { borderColor: "#E10600", color: "#E10600", duration: 0.2 }, 37.48);
        tl.fromTo("#pt2", { scale: 1 }, { scale: 1.15, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }, 37.5);
        tl.to("#pt2", { borderColor: "rgba(255,255,255,0.35)", color: "rgba(255,255,255,0.55)", duration: 0.2 }, 40.5);
        [[0, 42.58, 46.0], [1, 46.0, 49.36], [2, 49.36, 57.6]].forEach(([n, a, z]) => {
          tl.to("#pt" + n, { backgroundColor: "#E10600", borderColor: "#E10600", color: "#FFFFFF", scale: 1.1, duration: 0.2 }, a);
          tl.fromTo("#pl" + n, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, ease: IN }, a + 0.05);
          if (n < 2) {
            tl.to("#pt" + n, { backgroundColor: "rgba(11,11,12,0.72)", borderColor: "rgba(255,255,255,0.35)", color: "rgba(255,255,255,0.55)", scale: 1, duration: 0.15 }, z - 0.05);
            tl.to("#pl" + n, { opacity: 0, duration: 0.12 }, z - 0.1);
          }
        });
        tl.to("#oP .pts", { opacity: 0, duration: 0.15 }, 57.6);
        // N: prescription
        cut("#cN", 40.76, 42.58);
        tl.fromTo("#cNrx", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }, 40.78);
        tl.fromTo("#cNg", { opacity: 0 }, { opacity: 0.6, duration: 0.12, yoyo: true, repeat: 1 }, 41.0);
        rise("#cN .kk", 40.85); rise("#cNt", 41.24);
        // O: side effects
        cut("#cO", 46.0, 49.36);
        rise("#cO .kk", 46.1); pop("#cO0", 46.54); pop("#cO1", 47.14);
        tl.fromTo(["#cO0", "#cO1"], { rotation: 0 }, { keyframes: [{ rotation: -2, duration: 0.08 }, { rotation: 2, duration: 0.08 }, { rotation: 0, duration: 0.08 }] }, 48.4);
        // P: what the trial did
        cut("#cP", 49.36, 53.92);
        rise("#cP .kk", 49.45);
        pop("#cP0", 50.0); pop("#cPo0", 50.9); pop("#cP1", 51.2); pop("#cPo1", 52.0); pop("#cP2", 52.3); pop("#cPo2", 52.9);
        tl.fromTo("#cP3", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.in" }, 53.05);
        // Q: scale vs muscle
        cut("#cQ", 53.92, 57.76);
        pop("#cQ0", 54.0, 0.8);
        tl.fromTo("#cQn", { rotation: 55 }, { rotation: -55, duration: 1.4, ease: "power2.inOut" }, 54.4);
        pop("#cQ1", 55.6, 0.8);
        tl.fromTo("#cQq", { scale: 1 }, { scale: 1.2, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }, 56.32);
        // R: resistance training
        cut("#cR", 57.76, 60.5);
        tl.fromTo("#cRt", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: SET }, 58.24);
        tl.fromTo("#cRd", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: IN }, 59.42);
        // T: ads + hype struck
        pop("#oT0", 63.2); strikeX("#oT0 .x", 63.5); pop("#oT1", 64.05); strikeX("#oT1 .x", 64.3);
        tl.to("#oT .band", { opacity: 0, y: -14, duration: 0.15, ease: OUT }, 65.75);
        // U: sustained results
        cut("#cU", 65.95, 70.85);
        rise("#cU .kk", 66.05); pop("#cU0", 67.3);
        pop("#cU1", 68.89); pop("#cUo", 69.5); pop("#cU2", 69.81);
      })();
