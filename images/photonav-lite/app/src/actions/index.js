import axios from 'axios'

export const MOVE_PHOTO_TO_ROW = 'MOVE_PHOTO_TO_ROW'
export const SET_CURSOR = 'SET_CURSOR'
export const MOVE_CURSOR = 'MOVE_CURSOR'


export function movePhotoToRow(
  i, j
) {
  return {
    type: MOVE_PHOTO_TO_ROW,
    payload: {i, j}
  }
}

export function setCursor(i) {
  console.log('selecting photo', i)
  return {
    type: SET_CURSOR,
    payload: i
  }
}

export function moveCursor(
  direction // right or left
) {
  return {
    type: MOVE_CURSOR,
    payload: direction
  }
}
