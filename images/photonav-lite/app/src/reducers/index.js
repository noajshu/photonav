import axios from 'axios'
import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form'

const REHYDRATE = 'persist/REHYDRATE'
import { SET_CURSOR, MOVE_PHOTO_TO_ROW, MOVE_CURSOR, FETCH_PHOTOS } from '../actions'


export const numRows = 2


function getUpMovedPosition(
  photos, cursor
) {
  const currentRow = photos[cursor].row
  const indexInCurrentRow = _.sum(_.range(0, cursor + 1).map(
    i => (photos[i].row == currentRow ? 1 : 0)
  ))
  let i = 0
  let iAbove = 0
  while (true) {
    if (i >= photos.length) {
      return -1
    }
    if (photos[i].row == currentRow - 1) {
      iAbove ++
    }
    if (iAbove == indexInCurrentRow){
      break
    }
    i ++
  }
  return i
}

function getDownMovedPosition(
  photos, cursor
) {
  const currentRow = photos[cursor].row
  const indexInCurrentRow = _.sum(_.range(0, cursor + 1).map(
    i => (photos[i].row == currentRow ? 1 : 0)
  ))
  let i = 0
  let iBelow = 0
  while (true) {
    if (i >= photos.length) {
      return -1
    }
    if (photos[i].row == currentRow + 1) {
      iBelow ++
    }
    if (iBelow == indexInCurrentRow){
      break
    }
    i ++
  }
  return i
}


function getRightMovedPosition(
  photos, cursor
) {
  const currentRow = photos[cursor].row
  for(let i=cursor + 1; i<photos.length; i++) {
    if (photos[i].row == currentRow) {
      return i
    }
  }
  return -1
}

function getLeftMovedPosition(
  photos, cursor
) {
  const currentRow = photos[cursor].row
  for(let i=cursor -1; i >= 0; i--) {
    if (photos[i].row == currentRow) {
      return i
    }
  }
  return -1
}


function gridReducer(
  state={
    cursor: 0,
    photos: [
      {url: '/img/0.jpg', row: 0},
      {url: '/img/0.jpg', row: 1},
      {url: '/img/0.jpg', row: 0},
      {url: '/img/1.jpg', row: 2},
      {url: '/img/0.jpg', row: 2},
      {url: '/img/1.jpg', row: 0},
      {url: '/img/0.jpg', row: 0},
      {url: '/img/0.jpg', row: 4},
      {url: '/img/1.jpg', row: 3},
      {url: '/img/0.jpg', row: 0},
      {url: '/img/0.jpg', row: 4},
      {url: '/img/0.jpg', row: 0},
      {url: '/img/1.jpg', row: 1},
      {url: '/img/1.jpg', row: 1},
      {url: '/img/0.jpg', row: 3},
    ]
  },
  action
) {
  switch(action.type) {
    case FETCH_PHOTOS:
      return {
        ...state, photos: action.payload.photos.map(
          photoName => ({url: `http://localhost:7777/img/${photoName}`, row: 0})
        )
      }
    case REHYDRATE:
      return {...state, photos: [
        {url: '/img/0.jpg', row: 0},
        {url: '/img/0.jpg', row: 1},
        {url: '/img/0.jpg', row: 0},
        {url: '/img/1.jpg', row: 2},
        {url: '/img/0.jpg', row: 2},
        {url: '/img/1.jpg', row: 0},
        {url: '/img/0.jpg', row: 0},
        {url: '/img/0.jpg', row: 4},
        {url: '/img/1.jpg', row: 3},
        {url: '/img/0.jpg', row: 0},
        {url: '/img/0.jpg', row: 4},
        {url: '/img/0.jpg', row: 0},
        {url: '/img/1.jpg', row: 1},
        {url: '/img/1.jpg', row: 1},
        {url: '/img/0.jpg', row: 3},
      ]
    }
    case MOVE_PHOTO_TO_ROW:
      if (action.payload.j < numRows && action.payload.j >= 0) {
        let photos = state.photos.slice()
        photos[action.payload.i].row = action.payload.j
        return {...state, photos}
      }
      return state
    case SET_CURSOR:
      return {
        ...state,
        cursor: action.payload
      }
    case MOVE_CURSOR:
      let newPosition = -1
      switch(action.payload) {
        case 'right':
          // newPosition = getRightMovedPosition(
          //   state.photos,
          //   state.cursor
          // )
          newPosition = state.cursor + 1
          break
        case 'left':
          // newPosition = getLeftMovedPosition(
          //   state.photos,
          //   state.cursor
          // )
          newPosition = state.cursor - 1
          break
        case 'up':
          // newPosition = getUpMovedPosition(
          //   state.photos,
          //   state.cursor
          // )
          break
        case 'down':
          // newPosition = getDownMovedPosition(
          //   state.photos,
          //   state.cursor
          // )
          break
      }
      console.log('in reducer, newPosition = ', newPosition)
      return {...state, cursor: (newPosition != -1 ? newPosition : state.cursor)}
    default:
      return state
  }
}

const rootReducer = combineReducers({
  grid: gridReducer
});

export default rootReducer;
