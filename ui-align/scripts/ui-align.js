// ui-align — live-DOM alignment measurement library.
// Evaluate this whole file in the target page (e.g. via claude-in-chrome
// javascript_tool). It installs `window.__uiAlign` and returns "ui-align loaded".
// All Y values are absolute page-viewport CSS px, rounded to 2 decimals.
//
// API:
//   __uiAlign.audit(selector)            -> full measurement report (JSON-safe)
//   __uiAlign.baselineOf(textNode)       -> baseline Y (strut trick, flex-safe)
//   __uiAlign.typeMetrics(el)            -> {cap, xh} canvas font metrics
//   __uiAlign.inkCentreY(svg)            -> icon ink centre Y (viewBox+stroke corrected)
//   __uiAlign.enlarge(selector, K, guides) -> DOM-scaled clone stage (real re-raster)
//   __uiAlign.clearStage()               -> remove the stage
//   __uiAlign.tryFix(cssText)            -> inject <style id="__uiAlignFix"> override
//   __uiAlign.removeFix()                -> remove the override
//   __uiAlign.assertClean()              -> true iff no override present (run after reload)
(() => {
  const R = n => Math.round(n * 100) / 100
  const cx = document.createElement('canvas').getContext('2d')

  // Zero-size inline-block strut sits exactly on the baseline. Gotcha: inside a
  // flex/grid parent the strut becomes a flex item positioned by align-items and
  // returns garbage — wrap the text node in an inline-block span first to force
  // an inline formatting context, then restore the DOM.
  function baselineOf(textNode) {
    const p = textNode.parentElement
    const strut = document.createElement('span')
    strut.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline;'
    let y
    if (/flex|grid/.test(getComputedStyle(p).display)) {
      const wrap = document.createElement('span')
      wrap.style.cssText = 'display:inline-block;'
      p.insertBefore(wrap, textNode)
      wrap.appendChild(textNode)
      wrap.appendChild(strut)
      y = strut.getBoundingClientRect().top
      strut.remove(); p.insertBefore(textNode, wrap); wrap.remove()
    } else {
      p.insertBefore(strut, textNode.nextSibling)
      y = strut.getBoundingClientRect().top
      strut.remove()
    }
    return y
  }

  function typeMetrics(el) {
    const cs = getComputedStyle(el)
    cx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize}/${cs.lineHeight} ${cs.fontFamily}`
    return {
      cap: cx.measureText('H').actualBoundingBoxAscent, // cap height
      xh: cx.measureText('x').actualBoundingBoxAscent,  // x-height
    }
  }

  // Two corrections both required: getBBox() is in viewBox user units, so
  // subtract viewBox.y before scaling to screen (forgetting it is a phantom
  // multi-px error); and getBBox() excludes stroke, so stroked art extends
  // strokeWidth/2 past the geometry on every side.
  function inkCentreY(svg) {
    const r = svg.getBoundingClientRect()
    const vb = svg.viewBox.baseVal
    if (!vb || !vb.height) return null
    let bb
    try { bb = svg.getBBox() } catch { return null }
    const sw = Math.max(0, ...[...svg.querySelectorAll('*')]
      .map(p => parseFloat(getComputedStyle(p).strokeWidth) || 0))
    const inkTop = bb.y - sw / 2
    const inkBot = bb.y + bb.height + sw / 2
    return r.top + ((inkTop + inkBot) / 2 - vb.y) * (r.height / vb.height)
  }

  function pathOf(el, root) {
    const parts = []
    for (let e = el; e && e !== root.parentElement && parts.length < 4; e = e.parentElement) {
      const cls = [...e.classList].slice(0, 2).join('.')
      parts.unshift(e.tagName.toLowerCase() + (cls ? '.' + cls : ''))
    }
    return parts.join(' > ')
  }

  // Hint only: text inside a bordered/filled rounded box (pill, kbd chip, badge,
  // button) aligns by box centre, not baseline — the agent applies that judgment.
  function boxedAncestor(el, root) {
    for (let e = el; e && e !== root.parentElement; e = e.parentElement) {
      const cs = getComputedStyle(e)
      const bordered = parseFloat(cs.borderTopWidth) > 0
      const filled = parseFloat(cs.borderRadius) > 0 &&
        cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent'
      if (bordered || filled || /^(KBD|BUTTON)$/.test(e.tagName)) return e
    }
    return null
  }

  function audit(selector) {
    const root = document.querySelector(selector)
    if (!root) return { error: `no match: ${selector}` }

    const nodes = []
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT)
    for (let n; (n = walker.nextNode());) {
      if (!n.textContent.trim()) continue
      const p = n.parentElement
      if (!p || /^(SCRIPT|STYLE|NOSCRIPT)$/.test(p.tagName)) continue
      if (p.closest('#__uiAlignStage')) continue
      const r = p.getBoundingClientRect()
      if (!r.width || !r.height) continue
      nodes.push(n)
    }

    const text = nodes.map(n => {
      const p = n.parentElement
      const cs = getComputedStyle(p)
      const r = p.getBoundingClientRect()
      const baselineY = baselineOf(n)
      const { cap, xh } = typeMetrics(p)
      const boxCenterY = r.top + r.height / 2
      const capMidY = baselineY - cap / 2
      const boxed = boxedAncestor(p, root)
      return {
        text: n.textContent.trim().slice(0, 40),
        path: pathOf(p, root),
        fontSize: cs.fontSize,
        fontFamily: cs.fontFamily.split(',')[0].trim(),
        fontWeight: cs.fontWeight,
        boxTop: R(r.top), boxHeight: R(r.height),
        boxCenterY: R(boxCenterY),
        baselineY: R(baselineY),
        capMidY: R(capMidY),
        xMidY: R(baselineY - xh / 2),
        // positive = optical centre rides BELOW box centre (text sits low)
        capMidMinusBoxCenter: R(capMidY - boxCenterY),
        boxed: boxed ? pathOf(boxed, root) : null,
      }
    })

    const svgs = [...root.querySelectorAll('svg')]
      .filter(s => !s.closest('#__uiAlignStage'))
      .map(s => {
        const r = s.getBoundingClientRect()
        if (!r.width || !r.height) return null
        const ink = inkCentreY(s)
        const boxCenterY = r.top + r.height / 2
        const vb = s.viewBox.baseVal
        return {
          path: pathOf(s, root),
          boxTop: R(r.top), boxHeight: R(r.height),
          boxCenterY: R(boxCenterY),
          inkCenterY: ink === null ? null : R(ink),
          inkMinusBoxCenter: ink === null ? null : R(ink - boxCenterY),
          viewBox: vb && vb.height ? `${vb.x} ${vb.y} ${vb.width} ${vb.height}` : null,
          note: ink === null ? 'no viewBox or getBBox failed (hidden?)' : undefined,
        }
      }).filter(Boolean)

    const spread = a => a.length ? R(Math.max(...a) - Math.min(...a)) : null
    const groups = arr => {
      const m = new Map()
      arr.forEach(v => m.set(v, (m.get(v) || 0) + 1))
      return [...m.entries()].sort((a, b) => a[0] - b[0]).map(([y, count]) => ({ y, count }))
    }
    return {
      selector,
      text, svgs,
      summary: {
        capMidSpread: spread(text.map(t => t.capMidY)),   // headline metric
        boxCenterSpread: spread(text.map(t => t.boxCenterY)),
        baselines: groups(text.map(t => t.baselineY)),
      },
    }
  }

  // Screenshot zoom upsamples an already-downscaled capture — sub-pixel detail
  // is gone before you zoom. transform:scale on a live clone makes the browser
  // re-rasterize, so the detail is genuinely present. Screenshot the stage.
  // guides: [{y, color?, label?}] with y in absolute page px (from audit()).
  function enlarge(selector, K = 6, guides = []) {
    clearStage()
    const src = document.querySelector(selector)
    if (!src) return { error: `no match: ${selector}` }
    const r = src.getBoundingClientRect()
    const stage = document.createElement('div')
    stage.id = '__uiAlignStage'
    stage.style.cssText = `position:fixed;left:0;top:0;z-index:2147483647;overflow:hidden;` +
      `width:${r.width * K}px;height:${r.height * K}px;background:${getComputedStyle(document.body).backgroundColor};outline:2px solid magenta`
    const clone = src.cloneNode(true)
    clone.style.cssText += `;position:absolute;left:0;top:0;transform:scale(${K});transform-origin:top left;margin:0`
    stage.appendChild(clone)
    guides.forEach(g => {
      const line = document.createElement('div')
      line.style.cssText = `position:absolute;left:0;right:0;height:1px;` +
        `top:${(g.y - r.top) * K}px;background:${g.color || 'red'}`
      if (g.label) {
        const tag = document.createElement('span')
        tag.textContent = `${g.label} ${g.y}`
        tag.style.cssText = 'position:absolute;right:2px;bottom:1px;font:10px monospace;color:inherit;background:rgba(255,255,255,.7)'
        tag.style.color = g.color || 'red'
        line.appendChild(tag)
      }
      stage.appendChild(line)
    })
    document.body.appendChild(stage)
    return { stage: '#__uiAlignStage', width: r.width * K, height: r.height * K, K }
  }

  function clearStage() { document.getElementById('__uiAlignStage')?.remove() }

  function tryFix(cssText) {
    removeFix()
    const s = document.createElement('style')
    s.id = '__uiAlignFix'
    s.textContent = cssText
    document.head.appendChild(s)
    return 'fix injected — re-run audit() to confirm the numbers move'
  }
  function removeFix() { document.getElementById('__uiAlignFix')?.remove() }
  function assertClean() { return document.getElementById('__uiAlignFix') === null }

  window.__uiAlign = { baselineOf, typeMetrics, inkCentreY, audit, enlarge, clearStage, tryFix, removeFix, assertClean }
  return 'ui-align loaded'
})()
