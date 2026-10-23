/**
 * Evolution Ice Fishing - 100% Authentic Replica Engine
 * Powered by official extracted CDN sprite sheets, audio assets, and exact game physics.
 */

const TOTAL_SECTORS = 53;
const RAD_PER_SECTOR = (2 * Math.PI) / TOTAL_SECTORS;

// 53 Physical Sectors Configuration
const SECTOR_TYPES = [];
(function initSectors() {
  const blues = new Set([0, 15, 27, 40]);
  const oranges = new Set([7, 34]);
  const reds = new Set([46]);
  let leaf = true;

  for (let i = 0; i < TOTAL_SECTORS; i++) {
    if (reds.has(i)) {
      SECTOR_TYPES.push({ index: i, type: 'HugeReds', name: 'Huge Reds' });
    } else if (oranges.has(i)) {
      SECTOR_TYPES.push({ index: i, type: 'BigOranges', name: 'Big Oranges' });
    } else if (blues.has(i)) {
      SECTOR_TYPES.push({ index: i, type: 'LilBlues', name: 'Lil\' Blues' });
    } else {
      SECTOR_TYPES.push({ index: i, type: leaf ? 'Leaf1' : 'Leaf2', name: leaf ? 'Light Leaf' : 'Dark Leaf' });
      leaf = !leaf;
    }
  }
})();

// Real Audio Subsystem with Extracted Evolution Sound Files
class SoundFX {
  constructor() {
    this.enabled = true;
    this.lastFlapperTime = 0;
    this.sounds = {
      click: 'extracted_assets/audio/48kb.2ch.638981453302355.webm',
      chipPick: 'extracted_assets/audio/48kb.2ch.562582149641466.webm',
      chipPlace: 'extracted_assets/audio/48kb.2ch.575903920236274.webm',
      chipStack: 'extracted_assets/audio/48kb.2ch.973261462688918.webm',
      betLeaf1: 'extracted_assets/audio/48kb.2ch.707802841179452.webm',
      betBlue: 'extracted_assets/audio/48kb.2ch.491988489808681.webm',
      timerTick: 'extracted_assets/audio/48kb.2ch.872926799387045.webm',
      flapper: 'extracted_assets/audio/48kb.2ch.682449191389208.webm',
      snowFly: 'extracted_assets/audio/48kb.2ch.174768029172998.webm',
      snowHit: 'extracted_assets/audio/48kb.2ch.590161716721517.webm',
      winSmall: 'extracted_assets/audio/48kb.2ch.575670061204724.webm',
      winBig: 'extracted_assets/audio/48kb.2ch.666131434829669.webm',
      bonusWin: 'extracted_assets/audio/48kb.2ch.218026708514663.webm',
      rodEject: 'extracted_assets/audio/48kb.2ch.177316084430006.webm',
      rodReel: 'extracted_assets/audio/48kb.2ch.930588686202526.webm'
    };
  }

  play(name, vol = 1.0) {
    if (!this.enabled || !this.sounds[name]) return;
    try {
      const a = new Audio(this.sounds[name]);
      a.volume = Math.max(0, Math.min(1, vol));
      a.play().catch(() => {});
    } catch (e) {}
  }

  clickFlapper() {
    if (!this.enabled) return;
    const now = performance.now();
    if (now - this.lastFlapperTime > 28) {
      this.lastFlapperTime = now;
      this.play('flapper', 0.55);
    }
  }
}

class AuthenticIceFishingGame {
  constructor() {
    this.sfx = new SoundFX();
    this.canvas = document.getElementById('wheel-canvas');
    this.ctx = this.canvas.getContext('2d');
    this.needleEl = document.getElementById('flapper-needle');

    // Official Image Assets
    this.wheelImg = new Image();
    this.wheelImg.src = 'extracted_assets/game_ui/rotating_wheel_disc.png';
    this.wheelImgLoaded = false;
    this.wheelImg.onload = () => { this.wheelImgLoaded = true; };

    this.centerMedallion = new Image();
    this.centerMedallion.src = 'official_assets/sprites/center.png';
    this.centerMedallionLoaded = false;
    this.centerMedallion.onload = () => { this.centerMedallionLoaded = true; };

    this.goldLeafImg = new Image();
    this.goldLeafImg.src = 'official_assets/sprites/leaf-gold.png';

    // State Variables
    this.balance = 1000;
    this.selectedChip = 10;
    this.bets = { Leaf1: 0, Leaf2: 0, LilBlues: 0, BigOranges: 0, HugeReds: 0 };
    this.betStack = [];
    this.activeMultipliers = {}; // { sectorIndex: multiplierValue }

    // Physics
    this.wheelAngle = 0; // In radians
    this.isSpinning = false;
    this.targetSector = 0;
    this.lastPassedSector = -1;

    // Phase Loop
    this.phase = 'BETS_OPEN';
    this.countdown = 7;
    this.timer = null;

    // Chat Feed Data
    this.chatMessages = [
      { user: 'Dado12:', msg: 'Cmon really' },
      { user: 'rvijayvijayr:', msg: '🐟 🐟 🐟 🔥 100x pls' },
      { user: 'Alex_K:', msg: 'Huge reds overdue!' },
      { user: 'LuckyStar:', msg: 'Leaf 1 safe bet' },
      { user: 'CasinoKing:', msg: 'Big oranges next round' }
    ];
    this.chatIdx = 0;

    this.bindEvents();
    this.startChatTicker();
    this.startBettingRound();
    this.renderLoop();
  }

  bindEvents() {
    // Chip selection
    document.querySelectorAll('.chip-item').forEach(chip => {
      chip.onclick = () => {
        document.querySelectorAll('.chip-item').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        this.selectedChip = parseInt(chip.getAttribute('data-val'), 10);
        this.sfx.play('chipPick', 0.7);
      };
    });

    // Touch targets directly over the screenshot buttons
    document.querySelectorAll('.bet-touch-target').forEach(spot => {
      spot.onclick = () => {
        const spotName = spot.getAttribute('data-spot');
        this.placeBet(spotName, this.selectedChip);
      };
    });

    // Quick Actions
    document.getElementById('qa-undo').onclick = () => this.undoBet();
    document.getElementById('qa-double').onclick = () => this.doubleBets();
    document.getElementById('qa-all-bonuses').onclick = () => this.betAllBonuses();
    document.getElementById('qa-spin-now').onclick = () => {
      if (this.phase === 'BETS_OPEN') this.closeBetsAndSpin();
    };

    document.getElementById('btn-repeat').onclick = () => this.doubleBets();

    // Bonus Screen triggers
    document.getElementById('btn-reel-in').onclick = () => this.claimBonus();
    document.getElementById('bonus-hole-trigger').onclick = () => this.claimBonus();
  }

  placeBet(spot, amount) {
    if (this.phase !== 'BETS_OPEN') return;
    if (this.balance < amount) {
      this.sfx.play('click', 0.5);
      return;
    }

    this.balance -= amount;
    this.bets[spot] += amount;
    this.betStack.push({ spot, amount });

    this.sfx.play(spot.startsWith('Leaf') ? 'betLeaf1' : 'betBlue', 0.85);
    this.sfx.play('chipPlace', 0.6);
    this.updateUI();
  }

  undoBet() {
    if (this.phase !== 'BETS_OPEN' || !this.betStack.length) return;
    const last = this.betStack.pop();
    this.bets[last.spot] -= last.amount;
    this.balance += last.amount;
    this.sfx.play('click', 0.6);
    this.updateUI();
  }

  doubleBets() {
    if (this.phase !== 'BETS_OPEN') return;
    const total = Object.values(this.bets).reduce((a, b) => a + b, 0);
    if (total === 0 || this.balance < total) return;
    this.balance -= total;
    for (let k in this.bets) this.bets[k] *= 2;
    this.sfx.play('chipStack', 0.8);
    this.updateUI();
  }

  betAllBonuses() {
    if (this.phase !== 'BETS_OPEN') return;
    const totalNeeded = this.selectedChip * 3;
    if (this.balance < totalNeeded) return;
    ['LilBlues', 'BigOranges', 'HugeReds'].forEach(s => this.placeBet(s, this.selectedChip));
  }

  updateUI() {
    const totalBet = Object.values(this.bets).reduce((a, b) => a + b, 0);
    document.getElementById('total-bet-val').textContent = `₹${totalBet}`;
    document.getElementById('balance-val').textContent = `₹${this.balance.toLocaleString()}`;

    for (let spot in this.bets) {
      const holder = document.getElementById(`chip-spot-${spot}`);
      const val = this.bets[spot];
      if (val > 0) {
        holder.querySelector('.chip-token').textContent = `₹${val}`;
        holder.classList.remove('hidden');
      } else {
        holder.classList.add('hidden');
      }
    }
  }

  startChatTicker() {
    setInterval(() => {
      this.chatIdx = (this.chatIdx + 1) % this.chatMessages.length;
      const m = this.chatMessages[this.chatIdx];
      const el = document.getElementById('chat-ticker');
      el.innerHTML = `<span class="chat-user">${m.user}</span> <span class="chat-msg">${m.msg}</span>`;
    }, 4500);
  }

  startBettingRound() {
    this.phase = 'BETS_OPEN';
    this.countdown = 7;
    this.activeMultipliers = {};
    document.getElementById('golden-multipliers-layer').innerHTML = '';

    const banner = document.getElementById('status-banner');
    banner.className = 'status-banner open';
    document.getElementById('banner-text').textContent = 'PLACE YOUR BETS';
    document.getElementById('banner-timer').textContent = `${this.countdown}s`;
    document.getElementById('qa-spin-now').disabled = false;

    clearInterval(this.timer);
    this.timer = setInterval(() => {
      this.countdown--;
      document.getElementById('banner-timer').textContent = `${this.countdown}s`;
      if (this.countdown <= 4 && this.countdown > 0) {
        this.sfx.play('timerTick', 0.6);
      }
      if (this.countdown <= 0) {
        clearInterval(this.timer);
        this.closeBetsAndSpin();
      }
    }, 1000);
  }

  closeBetsAndSpin() {
    clearInterval(this.timer);
    this.phase = 'BETS_CLOSED';
    document.getElementById('qa-spin-now').disabled = true;

    const banner = document.getElementById('status-banner');
    banner.className = 'status-banner';
    document.getElementById('banner-text').textContent = 'BETS CLOSED';
    document.getElementById('banner-timer').textContent = '';

    setTimeout(() => {
      this.distributeSnowballMultipliers();
      this.startWheelSpin();
    }, 1000);
  }

  distributeSnowballMultipliers() {
    const count = 2 + Math.floor(Math.random() * 3);
    const multValues = [3, 3, 5, 7, 10];

    for (let i = 0; i < count; i++) {
      const sec = Math.floor(Math.random() * TOTAL_SECTORS);
      const val = multValues[Math.floor(Math.random() * multValues.length)];
      this.activeMultipliers[sec] = val;
    }

    this.sfx.play('snowFly', 0.7);
    setTimeout(() => {
      this.sfx.play('snowHit', 0.85);
      this.renderGoldenMultipliers();
    }, 450);
  }

  renderGoldenMultipliers() {
    const layer = document.getElementById('golden-multipliers-layer');
    layer.innerHTML = '';
    const cx = 186;
    const cy = 186;
    const r = 125;

    for (let sec in this.activeMultipliers) {
      const secIdx = parseInt(sec, 10);
      const angle = (secIdx * RAD_PER_SECTOR) + this.wheelAngle;
      const x = cx + Math.sin(angle) * r;
      const y = cy - Math.cos(angle) * r;

      const el = document.createElement('div');
      el.className = 'golden-mult-tag';
      el.style.left = `${x}px`;
      el.style.top = `${y}px`;
      el.innerHTML = `<img src="official_assets/sprites/leaf-gold.png" class="golden-leaf-img" alt="Leaf"><span>${this.activeMultipliers[sec]}x</span>`;
      layer.appendChild(el);
    }
  }

  startWheelSpin() {
    this.phase = 'SPINNING';
    const banner = document.getElementById('status-banner');
    banner.className = 'status-banner spinning';
    document.getElementById('banner-text').textContent = 'WHEEL SPINNING';

    this.targetSector = Math.floor(Math.random() * TOTAL_SECTORS);

    const turns = 6 + Math.floor(Math.random() * 3);
    const targetAngleOffset = (TOTAL_SECTORS - this.targetSector) * RAD_PER_SECTOR;

    this.startAngle = this.wheelAngle;
    this.endAngle = this.wheelAngle + (turns * 2 * Math.PI) + targetAngleOffset;
    this.spinDuration = 7200;
    this.spinStartTime = performance.now();
    this.isSpinning = true;
  }

  renderLoop() {
    const loop = () => {
      this.updateWheelPhysics();
      this.drawWheelDisc();
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  updateWheelPhysics() {
    if (!this.isSpinning) return;

    const elapsed = performance.now() - this.spinStartTime;
    const p = Math.min(1, elapsed / this.spinDuration);

    const ease = 1 - Math.pow(1 - p, 3.2);
    this.wheelAngle = this.startAngle + (this.endAngle - this.startAngle) * ease;

    const currentPeg = Math.floor((this.wheelAngle / RAD_PER_SECTOR) % TOTAL_SECTORS);
    if (currentPeg !== this.lastPassedSector) {
      this.lastPassedSector = currentPeg;
      this.sfx.clickFlapper();

      if (this.needleEl) {
        this.needleEl.style.transform = 'rotate(-16deg)';
        setTimeout(() => { this.needleEl.style.transform = 'rotate(0deg)'; }, 35);
      }
    }

    if (Object.keys(this.activeMultipliers).length > 0) {
      this.renderGoldenMultipliers();
    }

    if (p >= 1) {
      this.isSpinning = false;
      this.resolveLandedOutcome(this.targetSector);
    }
  }

  drawWheelDisc() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, 372, 372);

    ctx.save();
    ctx.translate(186, 186);
    ctx.rotate(this.wheelAngle);

    if (this.wheelImgLoaded) {
      ctx.drawImage(this.wheelImg, -186, -186, 372, 372);
    }

    // Draw crisp official 3D Ice Fishing medallion in center
    if (this.centerMedallionLoaded) {
      ctx.drawImage(this.centerMedallion, -50, -50, 100, 100);
    }

    ctx.restore();
  }

  resolveLandedOutcome(sectorIdx) {
    this.phase = 'RESULT';
    const sector = SECTOR_TYPES[sectorIdx];
    const mult = this.activeMultipliers[sectorIdx] || 1;

    const banner = document.getElementById('status-banner');
    banner.className = 'status-banner';
    document.getElementById('banner-text').textContent = 'NEXT GAME SOON';
    document.getElementById('banner-timer').textContent = '';

    if (['LilBlues', 'BigOranges', 'HugeReds'].includes(sector.type)) {
      this.sfx.play('bonusWin', 1.0);
      this.launchBonusMiniGame(sector, mult);
    } else {
      const betAmount = this.bets[sector.type] || 0;
      let payout = 0;
      if (betAmount > 0) {
        payout = betAmount * (1 + mult);
        this.balance += payout;
        this.sfx.play(mult > 1 ? 'winBig' : 'winSmall', 0.9);
      } else {
        this.sfx.play('winSmall', 0.4);
      }

      this.showWinModal(sector.name, `${mult}X`, payout);
      setTimeout(() => this.resetNextRound(), 3500);
    }
  }

  showWinModal(label, multText, payout) {
    const splash = document.getElementById('win-notification');
    document.getElementById('win-label').textContent = label;
    document.getElementById('win-multiplier-badge').textContent = multText;
    document.getElementById('win-amount-text').textContent = payout > 0 ? `+₹${payout}` : 'NO WIN';
    splash.classList.remove('hidden');

    setTimeout(() => {
      splash.classList.add('hidden');
    }, 2800);
  }

  launchBonusMiniGame(sector, baseMult) {
    this.bonusData = { sector, baseMult };
    const overlay = document.getElementById('bonus-overlay');
    document.getElementById('bonus-header-title').textContent = `${sector.name.toUpperCase()} BONUS`;
    document.getElementById('bonus-mult-reveal').textContent = '?';

    // Hook official jumping fish sprite
    const fishImg = document.getElementById('official-jumping-fish');
    if (sector.type === 'LilBlues') {
      fishImg.src = 'official_assets/images/lilbluesju.f094362e.webp';
    } else if (sector.type === 'BigOranges') {
      fishImg.src = 'official_assets/images/bigoranges.d52ffd05.webp';
    } else if (sector.type === 'HugeReds') {
      fishImg.src = 'official_assets/images/hugeredsju.ac33dde7.webp';
    }

    overlay.classList.remove('hidden');
    this.sfx.play('rodEject', 0.8);
  }

  claimBonus() {
    if (!this.bonusData) return;
    const { sector, baseMult } = this.bonusData;
    this.bonusData = null;

    this.sfx.play('rodReel', 0.9);

    let fishMult = 15;
    if (sector.type === 'LilBlues') fishMult = [15, 25, 50, 75][Math.floor(Math.random() * 4)];
    else if (sector.type === 'BigOranges') fishMult = [50, 100, 200, 300][Math.floor(Math.random() * 4)];
    else if (sector.type === 'HugeReds') fishMult = [250, 500, 1000, 2500][Math.floor(Math.random() * 4)];

    const totalMultiplier = fishMult * baseMult;
    document.getElementById('bonus-mult-reveal').textContent = `${totalMultiplier}X`;

    const betAmount = this.bets[sector.type] || 0;
    const payout = betAmount * totalMultiplier;
    this.balance += payout;

    setTimeout(() => {
      this.sfx.play('bonusWin', 1.0);
      setTimeout(() => {
        document.getElementById('bonus-overlay').classList.add('hidden');
        this.showWinModal(sector.name, `${totalMultiplier}X`, payout);
        setTimeout(() => this.resetNextRound(), 3500);
      }, 1600);
    }, 600);
  }

  resetNextRound() {
    for (let k in this.bets) this.bets[k] = 0;
    this.betStack = [];
    this.updateUI();
    this.startBettingRound();
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.game = new AuthenticIceFishingGame();
});
