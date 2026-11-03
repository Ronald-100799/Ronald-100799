      // ---------- custom layer (reel 10, Terrace): zooms stay inside the picture band; cute, subtle motion only ----------
      (function () {
        // the camera moves scale the picture inside its letterbox band, never into the black bars
        tl.set("#fx", { clipPath: "inset(598px 0px 599px 0px)" }, 0);
        tl.set("#fx", { clipPath: "inset(656px 0px 657px 0px)" }, 5.067);   // Ron's own reframe at 5.067 s

        // polaroid: drops in with a little swing, settles at its tilt; leaves by floating up
        function drop(sel, t, rot) {
          tl.fromTo(sel, { opacity: 0, y: -60, rotation: rot * 3 }, { opacity: 1, y: 0, rotation: rot, duration: 0.55, ease: "back.out(2)" }, t);
          tl.fromTo(sel, { rotation: rot }, { rotation: rot * 0.6, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false }, t + 0.55);
        }
        const leave = (sel, t) => tl.to(sel, { opacity: 0, y: -40, scale: 0.94, duration: 0.25, ease: "power2.in" }, t);
        const twinkle = (sel, t, n = 3) => tl.fromTo(sel, { scale: 0, rotation: 0, opacity: 0 }, { scale: 1, rotation: 90, opacity: 1, duration: 0.35, ease: "back.out(2.5)", yoyo: true, repeat: n, repeatDelay: 0.25 }, t);

        drop("#pA0", 0.05, -6); drop("#pA1", 1.14, 3); drop("#pA2", 1.6, -3);
        twinkle("#sA0", 0.5); twinkle("#sA1", 1.9);
        leave("#pA0", 4.6); leave("#pA1", 4.66); leave("#pA2", 4.72);

        tl.fromTo("#nWc", { opacity: 0, y: -30, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(2)" }, 17.66);
        tl.fromTo("#nWc .big", { rotation: -2 }, { rotation: 2, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false }, 18.1);
        twinkle("#sW0", 18.0, 2);
        leave("#nWc", 19.85);

        drop("#pS0", 21.6, 4); leave("#pS0", 23.9);
        drop("#pB0", 30.84, -4); leave("#pB0", 32.55);
        drop("#pE0", 32.9, 3); leave("#pE0", 35.75);
        drop("#pW0", 36.9, -3); leave("#pW0", 39.5);
        drop("#pK0", 45.54, 4); leave("#pK0", 47.95);
      })();
