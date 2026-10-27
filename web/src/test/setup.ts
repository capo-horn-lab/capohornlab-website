import '@testing-library/jest-dom/vitest'
import { configure } from '@testing-library/react'

// `findBy*` aspetta 1 s per default: con 4 suite in parallelo (valutazione 3) un import lazy respinto o un chunk
// simulato puo' arrivare dopo, e il test fallisce senza che il codice sia sbagliato. 10 s su tutta la suite.
configure({ asyncUtilTimeout: 10_000 })
