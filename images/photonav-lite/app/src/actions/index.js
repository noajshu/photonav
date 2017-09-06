import axios from 'axios'

export const MOVE_PHOTO_TO_ROW = 'MOVE_PHOTO_TO_ROW'
export const SET_CURSOR = 'SET_CURSOR'
export const MOVE_CURSOR = 'MOVE_CURSOR'
export const FETCH_PHOTOS = 'FETCH_PHOTOS'


const API_URL = 'http://localhost:7777'

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

export function fetchPhotos() {
  return dispatch => {
    axios.get(API_URL).then(
      response => {
        dispatch({
          type: FETCH_PHOTOS,
          payload: response.data
        })
      }
    )
  }
}