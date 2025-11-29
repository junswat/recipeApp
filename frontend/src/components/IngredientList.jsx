import React, { useState, useEffect } from 'react';

export default function IngredientList({ ingredients }) {
    const [checkedItems, setCheckedItems] = useState({});

    const toggleItem = (index) => {
        setCheckedItems(prev => ({
            ...prev,
            [index]: !prev[index]
        }));
    };

    return (
        <div className="ingredient-list">
            <ul>
                {ingredients.map((item, index) => (
                    <li key={index} className={checkedItems[index] ? 'checked' : ''} onClick={() => toggleItem(index)}>
                        <input
                            type="checkbox"
                            checked={!!checkedItems[index]}
                            readOnly
                        />
                        <span className="amount">{item.amount} {item.unit}</span>
                        <span className="name">{item.name}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}
