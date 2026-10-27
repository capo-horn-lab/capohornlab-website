import { useEffect, useState } from 'react'

/** True from the frame after the first paint: a chart's chunk (Bklit + Motion) is requested only once the page's text is on
 * screen, so the text does not wait for it (Lighthouse LCP and TBT on a phone). */
export function useDopoIlPrimoPaint(): boolean {
  const [pronto, setPronto] = useState(false)
  useEffect(() => {
    let t: ReturnType<typeof setTimeout> | undefined
    const id = requestAnimationFrame(() => (t = setTimeout(() => setPronto(true))))
    return () => {
      cancelAnimationFrame(id)
      clearTimeout(t)
    }
  }, [])
  return pronto
}
