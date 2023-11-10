import React, {useContext} from 'react';
import './Modal.css';
import { ModalContext } from '../App';

function Modal({open, title, message}) {
    const modalContext = useContext(ModalContext);
    if (open === false) {
        return null;
    }
    const closeModal = () => {
        modalContext.setModalOpen(false);
    }

  return (
    <div className='modalContainer'>
        <div className='modalOverlay' onClick={() => closeModal()}>
            <div className='modalContent'>
                <h2 id="modalTitle">{title}</h2>
                <button onClick={() => closeModal()} id='exitModalButton'>X</button>
                <p id="modalMessage">{message}</p>
            </div>
        </div>
    </div>
  )
}

export default Modal;