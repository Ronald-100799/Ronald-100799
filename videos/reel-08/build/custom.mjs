      import * as THREE from "./assets/three/three.module.min.js";
      const RED = new THREE.Color("#E10600"), WHITE = new THREE.Color("#f4f4f6"), INK = new THREE.Color("#141416"), STEEL = new THREE.Color("#9aa0a8");
      const clamp = (x) => Math.min(Math.max(x, 0), 1);
      const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
      const back = (x) => { x = clamp(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
      const mat = (color, r = 0.4, m = 0.2) => new THREE.MeshStandardMaterial({ color, roughness: r, metalness: m });
      function stage(id, w, h, cam) {
        const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById(id), alpha: true, antialias: true, preserveDrawingBuffer: true });
        renderer.setPixelRatio(1); renderer.setSize(w, h, false); renderer.setClearColor(0, 0);
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(30, w / h, 0.1, 50);
        camera.position.set(...cam); camera.lookAt(0, 0, 0);
        scene.add(new THREE.HemisphereLight(0xffffff, 0x200606, 1.5));
        const key = new THREE.DirectionalLight(0xfff3ea, 2.6); key.position.set(3, 4, 5); scene.add(key);
        const rim = new THREE.DirectionalLight(0xff4a3a, 2.0); rim.position.set(-4, 1, -4); scene.add(rim);
        return { renderer, scene, camera };
      }
      // generic injection pen (no brand design)
      const P = stage("penCv", 1000, 700, [0, 0.4, 9]);
      const pen = new THREE.Group();
      const addX = (g, geo, m, x) => { const o = new THREE.Mesh(geo, m); o.rotation.z = Math.PI / 2; o.position.x = x; g.add(o); return o; };
      addX(pen, new THREE.CylinderGeometry(0.42, 0.42, 3.4, 64), mat(WHITE, 0.35), 0);
      addX(pen, new THREE.CylinderGeometry(0.44, 0.44, 0.5, 64), mat(RED, 0.4), -0.55);
      addX(pen, new THREE.CylinderGeometry(0.46, 0.46, 1.3, 64), mat(INK, 0.5), -2.35);
      addX(pen, new THREE.CylinderGeometry(0.36, 0.42, 0.25, 64), mat(INK, 0.5), 1.82);
      addX(pen, new THREE.CylinderGeometry(0.34, 0.34, 0.5, 48), mat(RED, 0.45), 2.2);
      addX(pen, new THREE.CylinderGeometry(0.2, 0.2, 0.18, 32), mat(INK, 0.5), 2.54);
      for (let k = 0; k < 10; k++) { const r = addX(pen, new THREE.BoxGeometry(0.06, 0.5, 0.74), mat(INK, 0.5), 2.2); r.rotation.x = k * Math.PI / 10; }
      const clip = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.12, 0.16), mat(INK, 0.4)); clip.position.set(-2.3, 0.5, 0); pen.add(clip);
      const win = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.26, 0.1), mat(new THREE.Color("#2a2a2e"), 0.15, 0.1)); win.position.set(0.55, 0, 0.42); pen.add(win);
      P.scene.add(pen);
      // STEP 1 bars: semaglutide −14.9% (red) vs placebo −2.4% (white), growing downward from a baseline
      const B = stage("barsCv", 900, 560, [0, 0.9, 9.5]);
      const barG = new THREE.Group(); barG.position.y = 1.35; B.scene.add(barG);
      const base = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.05, 1.8), mat(WHITE, 0.6)); barG.add(base);
      const bars = [[14.9, RED, -1.25], [2.4, WHITE, 1.25]].map(([v, c, x]) => {
        const m = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1, 1.5), mat(c, 0.45, 0.1));
        m.position.x = x; m.userData.h = 2.9 * v / 14.9; barG.add(m); return m;
      });
      // dumbbell for resistance training
      const Dm = stage("dbCv", 1000, 640, [0, 0.5, 8.4]);
      const db = new THREE.Group();
      addX(db, new THREE.CylinderGeometry(0.09, 0.09, 2.6, 32), mat(STEEL, 0.3, 0.7), 0);
      for (const sx of [-1, 1]) for (const [off, r, w, c] of [[0.62, 0.66, 0.2, RED], [0.84, 0.52, 0.18, INK], [1.04, 0.38, 0.16, INK]]) addX(db, new THREE.CylinderGeometry(r, r, w, 64), mat(c, 0.5, 0.2), sx * off);
      Dm.scene.add(db);

      const fmt = (n) => "₹" + Math.round(n).toLocaleString("en-IN");
      function renderAt(T) {
        // price counter: ₹0 → ₹1,300 landing on the spoken "1300" at 6.22
        const pc = document.getElementById("cDp");
        if (pc) pc.textContent = fmt(1300 * ease((T - 5.55) / 0.67));
        const tp = T - 3.66;
        if (tp > -0.05 && tp < 1.8) {
          pen.scale.setScalar(Math.max(0.85 * back(tp / 0.45), 0.001));
          pen.rotation.set(0.15 + 0.08 * Math.sin(tp * 2), -1.3 + 1.4 * ease(tp / 0.8) + 0.25 * tp, 0.12 - 0.1 * ease(tp / 0.8));
          P.renderer.render(P.scene, P.camera);
        }
        const tb = T - 26.93;
        if (tb > -0.05 && tb < 4.3) {
          barG.rotation.y = -0.3 + 0.06 * tb; barG.rotation.x = 0.12;
          bars.forEach((m, i) => { const k = ease((tb - 1.1 - (1 - i) * 0.25) / 0.65); m.scale.y = Math.max(0.001, m.userData.h * k); m.position.y = -m.scale.y / 2; });
          B.renderer.render(B.scene, B.camera);
          const v = document.getElementById("cKv0");
          if (v) v.textContent = "−" + (14.9 * ease((tb - 1.1) / 0.65)).toFixed(1) + "%";
        }
        const td = T - 57.76;
        if (td > -0.05 && td < 2.8) {
          db.scale.setScalar(Math.max(back(td / 0.5), 0.001));
          db.rotation.set(0.35 + 0.06 * Math.sin(td * 2), -1.2 + 1.2 * ease(td / 0.9) + 0.35 * td, -0.25);
          db.position.y = 0.12 * Math.sin(td * 2.4);
          Dm.renderer.render(Dm.scene, Dm.camera);
        }
      }
      window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
      renderAt(window.__hfThreeTime || 0);
